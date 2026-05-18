"""Offline PDF ingestion CLI for the first Phase 2 slice."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from contracts import ProcessedDocument


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


def build_processed_document(
    *,
    source_pdf_path: Path,
    markdown_output_path: Path,
    processed_output_path: Path,
    ingestion_status: str,
    error_message: str | None = None,
) -> ProcessedDocument:
    """Build one deterministic processed-document record."""

    source_pdf_id = source_pdf_path.stem
    return ProcessedDocument(
        source_pdf_id=source_pdf_id,
        source_pdf_path=str(source_pdf_path),
        markdown_output_path=str(markdown_output_path),
        processed_output_path=str(processed_output_path),
        document_name=source_pdf_id,
        document_version=None,
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


def ingest_one_pdf(
    *,
    source_pdf_path: Path,
    markdown_dir: Path,
    processed_dir: Path,
    overwrite: bool,
) -> ProcessedDocument:
    """Ingest one source PDF according to the deterministic storage rules."""

    markdown_output_path = markdown_dir / f"{source_pdf_path.stem}.md"
    processed_output_path = processed_dir / f"{source_pdf_path.stem}.json"

    if not overwrite and markdown_output_path.exists() and processed_output_path.exists():
        return build_processed_document(
            source_pdf_path=source_pdf_path,
            markdown_output_path=markdown_output_path,
            processed_output_path=processed_output_path,
            ingestion_status="skipped",
        )

    markdown_text = convert_pdf_to_markdown(source_pdf_path)
    markdown_output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_output_path.write_text(markdown_text, encoding="utf-8")

    record = build_processed_document(
        source_pdf_path=source_pdf_path,
        markdown_output_path=markdown_output_path,
        processed_output_path=processed_output_path,
        ingestion_status="succeeded",
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
            record = build_processed_document(
                source_pdf_path=source_pdf_path,
                markdown_output_path=markdown_dir / f"{source_pdf_path.stem}.md",
                processed_output_path=processed_dir / f"{source_pdf_path.stem}.json",
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
