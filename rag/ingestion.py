"""Offline PDF ingestion CLI for the current Phase 2 and early Phase 3 slices."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from contracts import ChunkBundle, ChunkRecord, ProcessedDocument

VERSION_PATTERN = re.compile(r"(?i)\b(?:version|versión)\b[:\s-]*([A-Za-z0-9][A-Za-z0-9._/-]*)")
EMPTY_BOILERPLATE_LINES = {"[]", "[ ]", "[]()", "![]()", "<!-- image -->"}
CHUNK_SCHEMA_VERSION = "v2"
DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 200
CLAUSE_LIKE_PATTERN = re.compile(r"^(?:\d+[.)]|[A-Z][.)]|[IVXLCDM]+[.)])(?:\s+\S.*)?$")
MAX_STRUCTURAL_BLOCK_LENGTH = 120


@dataclass(frozen=True)
class MarkdownBlock:
    """One deterministic cleaned-markdown block with structural context."""

    text: str
    section: str | None
    section_path: tuple[str, ...]
    kind: str


def parse_bool(value: str) -> bool:
    """Parse CLI boolean flags from explicit true/false strings."""

    normalized_value = value.strip().lower()
    if normalized_value == "true":
        return True
    if normalized_value == "false":
        return False
    raise argparse.ArgumentTypeError("expected 'true' or 'false'")


def parse_positive_int(value: str) -> int:
    """Parse a strictly positive integer CLI value."""

    parsed_value = int(value)
    if parsed_value < 1:
        raise argparse.ArgumentTypeError("expected an integer >= 1")
    return parsed_value


def parse_non_negative_int(value: str) -> int:
    """Parse a non-negative integer CLI value."""

    parsed_value = int(value)
    if parsed_value < 0:
        raise argparse.ArgumentTypeError("expected an integer >= 0")
    return parsed_value


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
    ingest_parser.add_argument("--chunk-size", type=parse_positive_int, default=DEFAULT_CHUNK_SIZE)
    ingest_parser.add_argument(
        "--chunk-overlap",
        type=parse_non_negative_int,
        default=DEFAULT_CHUNK_OVERLAP,
    )
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


def detect_block_kind(block_text: str) -> str:
    """Classify a cleaned-markdown block using deterministic local rules."""

    first_line = block_text.splitlines()[0].strip()
    if first_line.startswith("#"):
        return "heading"
    if "\n" not in block_text and CLAUSE_LIKE_PATTERN.match(first_line):
        return "clause_marker"
    return "paragraph"


def split_markdown_blocks(cleaned_markdown_text: str) -> list[MarkdownBlock]:
    """Split cleaned markdown into deterministic text blocks with structural context."""

    heading_stack: list[str] = []
    blocks: list[MarkdownBlock] = []

    for raw_block in cleaned_markdown_text.strip().split("\n\n"):
        block = raw_block.strip()
        if not block:
            continue
        first_line = block.splitlines()[0].strip()
        if first_line.startswith("#"):
            level = len(first_line) - len(first_line.lstrip("#"))
            heading_text = first_line.lstrip("#").strip()
            if heading_text:
                while len(heading_stack) >= level:
                    heading_stack.pop()
                heading_stack.append(heading_text)
        section = heading_stack[-1] if heading_stack else None
        blocks.append(
            MarkdownBlock(
                text=block,
                section=section,
                section_path=tuple(heading_stack),
                kind=detect_block_kind(block),
            )
        )

    return blocks


def expand_large_blocks(
    blocks: list[MarkdownBlock],
    chunk_size: int,
) -> list[MarkdownBlock]:
    """Split oversized blocks deterministically to respect chunk size."""

    expanded_blocks: list[MarkdownBlock] = []

    for block in blocks:
        if len(block.text) <= chunk_size:
            expanded_blocks.append(block)
            continue

        start = 0
        while start < len(block.text):
            expanded_blocks.append(
                MarkdownBlock(
                    text=block.text[start : start + chunk_size],
                    section=block.section,
                    section_path=block.section_path,
                    kind=block.kind,
                )
            )
            start += chunk_size

    return expanded_blocks


def can_merge_structural_pair(
    current_block: MarkdownBlock,
    next_block: MarkdownBlock,
    chunk_size: int,
) -> bool:
    """Return whether two neighboring blocks should be kept together."""

    combined_length = len(current_block.text) + 2 + len(next_block.text)
    if combined_length > chunk_size:
        return False
    if current_block.kind == "heading":
        return True
    if current_block.kind == "clause_marker":
        return True
    return (
        len(current_block.text) <= MAX_STRUCTURAL_BLOCK_LENGTH
        and next_block.section_path == current_block.section_path
    )


def group_semantic_blocks(blocks: list[MarkdownBlock], chunk_size: int) -> list[MarkdownBlock]:
    """Group related structural blocks before chunk assembly."""

    grouped_blocks: list[MarkdownBlock] = []
    index = 0

    while index < len(blocks):
        current_block = blocks[index]
        if index + 1 < len(blocks):
            next_block = blocks[index + 1]
            if can_merge_structural_pair(current_block, next_block, chunk_size):
                grouped_blocks.append(
                    MarkdownBlock(
                        text=f"{current_block.text}\n\n{next_block.text}",
                        section=next_block.section or current_block.section,
                        section_path=next_block.section_path or current_block.section_path,
                        kind="grouped",
                    )
                )
                index += 2
                continue
        grouped_blocks.append(current_block)
        index += 1

    return grouped_blocks


def build_chunk_records(
    *,
    source_pdf_id: str,
    document_name: str,
    document_version: str | None,
    source_pdf_path: Path,
    cleaned_markdown_output_path: Path,
    cleaned_markdown_text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[ChunkRecord]:
    """Build deterministic chunk records from cleaned markdown text."""

    blocks = expand_large_blocks(
        group_semantic_blocks(split_markdown_blocks(cleaned_markdown_text), chunk_size),
        chunk_size,
    )
    if not blocks:
        raise RuntimeError("No cleaned markdown blocks were available for chunk generation.")

    chunk_records: list[ChunkRecord] = []
    start_index = 0
    chunk_index = 0

    while start_index < len(blocks):
        current_entries: list[MarkdownBlock] = []
        current_length = 0
        end_index = start_index

        while end_index < len(blocks):
            block = blocks[end_index]
            separator_length = 2 if current_entries else 0
            next_length = current_length + separator_length + len(block.text)
            if current_entries and next_length > chunk_size:
                break
            current_entries.append(block)
            current_length = next_length
            end_index += 1

        chunk_text = "\n\n".join(entry.text for entry in current_entries)
        chunk_section = next(
            (entry.section for entry in reversed(current_entries) if entry.section),
            None,
        )
        chunk_section_path = next(
            (list(entry.section_path) for entry in reversed(current_entries) if entry.section_path),
            [],
        )
        chunk_records.append(
            ChunkRecord(
                chunk_id=f"{source_pdf_id}:{CHUNK_SCHEMA_VERSION}:{chunk_index:04d}",
                source_pdf_id=source_pdf_id,
                document_name=document_name,
                document_version=document_version,
                source_pdf_path=str(source_pdf_path),
                cleaned_markdown_output_path=str(cleaned_markdown_output_path),
                text=chunk_text,
                chunk_index=chunk_index,
                chunk_schema_version=CHUNK_SCHEMA_VERSION,
                section=chunk_section,
                section_path=chunk_section_path,
            )
        )
        chunk_index += 1

        if end_index >= len(blocks):
            break

        overlap_block_count = 0
        overlap_length = 0
        cursor = len(current_entries) - 1
        while cursor >= 0 and overlap_length < chunk_overlap:
            overlap_length += len(current_entries[cursor].text)
            overlap_block_count += 1
            cursor -= 1

        next_start_index = end_index - overlap_block_count
        start_index = max(next_start_index, start_index + 1)

    return chunk_records


def build_chunk_bundle(
    *,
    processed_document: ProcessedDocument,
    chunk_artifact_path: Path,
    cleaned_markdown_text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> ChunkBundle:
    """Build a deterministic chunk bundle for one processed document."""

    chunk_records = build_chunk_records(
        source_pdf_id=processed_document.source_pdf_id,
        document_name=processed_document.document_name,
        document_version=processed_document.document_version,
        source_pdf_path=Path(processed_document.source_pdf_path),
        cleaned_markdown_output_path=Path(processed_document.cleaned_markdown_output_path),
        cleaned_markdown_text=cleaned_markdown_text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return ChunkBundle(
        source_pdf_id=processed_document.source_pdf_id,
        document_name=processed_document.document_name,
        document_version=processed_document.document_version,
        source_pdf_path=processed_document.source_pdf_path,
        cleaned_markdown_output_path=processed_document.cleaned_markdown_output_path,
        chunk_artifact_path=str(chunk_artifact_path),
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        chunk_schema_version=CHUNK_SCHEMA_VERSION,
        chunks=chunk_records,
    )


def write_chunk_bundle(chunk_bundle: ChunkBundle, chunk_artifact_path: Path) -> None:
    """Persist a deterministic chunk bundle to JSON."""

    chunk_artifact_path.parent.mkdir(parents=True, exist_ok=True)
    chunk_artifact_path.write_text(chunk_bundle.model_dump_json(indent=2), encoding="utf-8")


def ingest_one_pdf(
    *,
    source_pdf_path: Path,
    markdown_dir: Path,
    processed_dir: Path,
    overwrite: bool,
    chunk_size: int,
    chunk_overlap: int,
) -> ProcessedDocument:
    """Ingest one source PDF according to the deterministic storage rules."""

    markdown_output_path = markdown_dir / f"{source_pdf_path.stem}.md"
    cleaned_markdown_output_path = processed_dir / f"{source_pdf_path.stem}.cleaned.md"
    processed_output_path = processed_dir / f"{source_pdf_path.stem}.json"
    chunk_artifact_path = processed_dir / "chunks" / f"{source_pdf_path.stem}.chunks.json"

    if (
        not overwrite
        and markdown_output_path.exists()
        and cleaned_markdown_output_path.exists()
        and processed_output_path.exists()
        and chunk_artifact_path.exists()
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
    chunk_bundle = build_chunk_bundle(
        processed_document=record,
        chunk_artifact_path=chunk_artifact_path,
        cleaned_markdown_text=cleaned_markdown_text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    write_chunk_bundle(chunk_bundle, chunk_artifact_path)
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
                chunk_size=args.chunk_size,
                chunk_overlap=args.chunk_overlap,
            )
        except Exception as exc:
            encountered_failures = True
            cleaned_markdown_output_path = processed_dir / f"{source_pdf_path.stem}.cleaned.md"
            processed_output_path = processed_dir / f"{source_pdf_path.stem}.json"
            chunk_artifact_path = processed_dir / "chunks" / f"{source_pdf_path.stem}.chunks.json"
            remove_artifact_if_exists(cleaned_markdown_output_path)
            remove_artifact_if_exists(processed_output_path)
            remove_artifact_if_exists(chunk_artifact_path)
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
    """CLI entrypoint for the current Phase 2 and Phase 3 chunking pipeline."""

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
