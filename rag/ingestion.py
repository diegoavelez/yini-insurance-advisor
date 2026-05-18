"""Offline PDF ingestion CLI for the current Phase 2 processing slices."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from contracts import ProcessedDocument

VERSION_PATTERN = re.compile(r"(?i)\b(?:version|versión)\b[:\s-]*([A-Za-z0-9][A-Za-z0-9._/-]*)")
EMPTY_BOILERPLATE_LINES = {"[]", "[ ]", "[]()", "![]()", "<!-- image -->"}


def parse_bool(value: str) -> bool:
    """Parse CLI boolean flags from explicit true/false strings."""

    normalized_value = value.strip().lower()
    if normalized_value == "true":
        return True
    if normalized_value == "false":
        return False
    raise argparse.ArgumentTypeError("expected 'true' or 'false'")


def build_parser() -> argparse.ArgumentParser:
    """Build the canonical ingestion CLI parser."""

    parser = argparse.ArgumentParser(prog="python -m rag.ingestion")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest-pdfs")
    ingest_parser.add_argument("--input-dir", required=True)
    ingest_parser.add_argument("--markdown-dir", required=True)
    ingest_parser.add_argument("--processed-dir", required=True)
    ingest_parser.add_argument("--manifest-path", required=True)
    ingest_parser.add_argument("--glob", default="*.pdf")
    ingest_parser.add_argument("--overwrite", type=parse_bool, default=False)
    ingest_parser.add_argument("--fail-fast", type=parse_bool, default=False)
    return parser


def docling_is_available() -> bool:
    """Return whether Docling is importable in the current runtime."""

    return importlib.util.find_spec("docling") is not None


def ensure_docling_available() -> None:
    """Fail loudly when Docling is not available locally."""

    if not docling_is_available():
        raise RuntimeError(
            "Docling is not installed. Install project dependencies before running "
            "the ingestion CLI."
        )


def convert_pdf_to_markdown(source_pdf_path: Path) -> str:
    """Convert one PDF to markdown through Docling."""

    from docling.document_converter import DocumentConverter

    converter = DocumentConverter()
    result = converter.convert(str(source_pdf_path))

    document = getattr(result, "document", None)
    if document is not None and hasattr(document, "export_to_markdown"):
        return document.export_to_markdown()

    markdown = getattr(result, "markdown", None)
    if isinstance(markdown, str) and markdown.strip():
        return markdown

    raise RuntimeError("Docling conversion result did not expose markdown output.")


def clean_markdown(markdown_text: str) -> str:
    """Apply conservative, deterministic cleaning to Docling markdown."""

    normalized_text = markdown_text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned_lines: list[str] = []
    previous_line_blank = False

    for raw_line in normalized_text.split("\n"):
        line = raw_line.rstrip()
        stripped_line = line.strip()

        if stripped_line in EMPTY_BOILERPLATE_LINES:
            continue

        if not stripped_line:
            if previous_line_blank:
                continue
            cleaned_lines.append("")
            previous_line_blank = True
            continue

        cleaned_lines.append(line)
        previous_line_blank = False

    cleaned_text = "\n".join(cleaned_lines).strip()
    if not cleaned_text:
        raise RuntimeError("Cleaned markdown is empty after conservative processing.")
    return f"{cleaned_text}\n"


def extract_document_metadata(
    source_pdf_path: Path,
    cleaned_markdown_text: str,
) -> tuple[str, str | None]:
    """Extract low-risk document metadata or return deterministic fallbacks."""

    document_name = source_pdf_path.stem
    document_version = None

    for line in cleaned_markdown_text.splitlines()[:20]:
        stripped_line = line.strip()
        if stripped_line.startswith("#"):
            heading_text = stripped_line.lstrip("#").strip()
            if heading_text:
                document_name = heading_text
                break

    version_match = VERSION_PATTERN.search("\n".join(cleaned_markdown_text.splitlines()[:40]))
    if version_match:
        document_version = version_match.group(1)

    return document_name, document_version


def build_processed_document(
    *,
    source_pdf_path: Path,
    markdown_output_path: Path,
    cleaned_markdown_output_path: Path,
    processed_output_path: Path,
    ingestion_status: str,
    document_name: str | None = None,
    document_version: str | None = None,
    error_message: str | None = None,
) -> ProcessedDocument:
    """Build one deterministic processed-document record."""

    source_pdf_id = source_pdf_path.stem
    return ProcessedDocument(
        source_pdf_id=source_pdf_id,
        source_pdf_path=str(source_pdf_path),
        markdown_output_path=str(markdown_output_path),
        cleaned_markdown_output_path=str(cleaned_markdown_output_path),
        processed_output_path=str(processed_output_path),
        document_name=document_name or source_pdf_id,
        document_version=document_version,
        ingestion_status=ingestion_status,
        error_message=error_message,
        ingested_at=datetime.now(UTC),
    )


def append_manifest_record(manifest_path: Path, record: ProcessedDocument) -> None:
    """Append one JSONL manifest record."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as manifest_file:
        manifest_file.write(record.model_dump_json())
        manifest_file.write("\n")


def write_processed_metadata(record: ProcessedDocument, processed_output_path: Path) -> None:
    """Write deterministic processed metadata for succeeded conversions."""

    processed_output_path.parent.mkdir(parents=True, exist_ok=True)
    processed_output_path.write_text(record.model_dump_json(indent=2), encoding="utf-8")


def iter_source_pdfs(input_dir: Path, glob_pattern: str) -> list[Path]:
    """Return sorted matching PDF files under the configured input directory."""

    return sorted(path for path in input_dir.glob(glob_pattern) if path.is_file())


def remove_artifact_if_exists(path: Path) -> None:
    """Delete an artifact path when it already exists."""

    if path.exists():
        path.unlink()


def ingest_one_pdf(
    *,
    source_pdf_path: Path,
    markdown_dir: Path,
    processed_dir: Path,
    overwrite: bool,
) -> ProcessedDocument:
    """Ingest one source PDF according to the deterministic storage rules."""

    markdown_output_path = markdown_dir / f"{source_pdf_path.stem}.md"
    cleaned_markdown_output_path = processed_dir / f"{source_pdf_path.stem}.cleaned.md"
    processed_output_path = processed_dir / f"{source_pdf_path.stem}.json"

    if (
        not overwrite
        and markdown_output_path.exists()
        and cleaned_markdown_output_path.exists()
        and processed_output_path.exists()
    ):
        return build_processed_document(
            source_pdf_path=source_pdf_path,
            markdown_output_path=markdown_output_path,
            cleaned_markdown_output_path=cleaned_markdown_output_path,
            processed_output_path=processed_output_path,
            ingestion_status="skipped",
        )

    raw_markdown_text = convert_pdf_to_markdown(source_pdf_path)
    markdown_output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_output_path.write_text(raw_markdown_text, encoding="utf-8")

    cleaned_markdown_text = clean_markdown(raw_markdown_text)
    document_name, document_version = extract_document_metadata(
        source_pdf_path,
        cleaned_markdown_text,
    )

    cleaned_markdown_output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_markdown_output_path.write_text(cleaned_markdown_text, encoding="utf-8")

    record = build_processed_document(
        source_pdf_path=source_pdf_path,
        markdown_output_path=markdown_output_path,
        cleaned_markdown_output_path=cleaned_markdown_output_path,
        processed_output_path=processed_output_path,
        ingestion_status="succeeded",
        document_name=document_name,
        document_version=document_version,
    )
    write_processed_metadata(record, processed_output_path)
    return record


def run_ingestion(args: argparse.Namespace) -> int:
    """Execute the CLI ingestion flow."""

    input_dir = Path(args.input_dir)
    markdown_dir = Path(args.markdown_dir)
    processed_dir = Path(args.processed_dir)
    manifest_path = Path(args.manifest_path)

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Input directory does not exist: {input_dir}", file=sys.stderr)
        return 2

    ensure_docling_available()

    source_pdfs = iter_source_pdfs(input_dir, args.glob)
    if not source_pdfs:
        print(
            f"No PDF files matched glob '{args.glob}' in input directory: {input_dir}",
            file=sys.stderr,
        )
        return 2

    encountered_failures = False

    for source_pdf_path in source_pdfs:
        try:
            record = ingest_one_pdf(
                source_pdf_path=source_pdf_path,
                markdown_dir=markdown_dir,
                processed_dir=processed_dir,
                overwrite=args.overwrite,
            )
        except Exception as exc:
            encountered_failures = True
            cleaned_markdown_output_path = processed_dir / f"{source_pdf_path.stem}.cleaned.md"
            processed_output_path = processed_dir / f"{source_pdf_path.stem}.json"
            remove_artifact_if_exists(cleaned_markdown_output_path)
            remove_artifact_if_exists(processed_output_path)
            record = build_processed_document(
                source_pdf_path=source_pdf_path,
                markdown_output_path=markdown_dir / f"{source_pdf_path.stem}.md",
                cleaned_markdown_output_path=cleaned_markdown_output_path,
                processed_output_path=processed_output_path,
                ingestion_status="failed",
                error_message=str(exc),
            )

        append_manifest_record(manifest_path, record)

        if record.ingestion_status == "failed":
            print(
                f"Failed to ingest {source_pdf_path.name}: {record.error_message}",
                file=sys.stderr,
            )
            if args.fail_fast:
                return 1

    return 0 if not (encountered_failures and args.fail_fast) else 1


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint for Phase 2 ingestion."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "ingest-pdfs":
        parser.error(f"Unsupported command: {args.command}")
    try:
        return run_ingestion(args)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
