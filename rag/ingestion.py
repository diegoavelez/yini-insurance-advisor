"""Offline PDF ingestion CLI for the current Phase 2 and early Phase 3 slices."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path

from contracts import (
    ChunkBundle,
    ChunkRecord,
    EmbeddingBundle,
    EmbeddingGenerationRecord,
    EmbeddingRecord,
    ProcessedDocument,
    VectorPayload,
)
from core.config import Settings, get_settings

VERSION_PATTERN = re.compile(r"(?i)\b(?:version|versión)\b[:\s-]*([A-Za-z0-9][A-Za-z0-9._/-]*)")
EMPTY_BOILERPLATE_LINES = {"[]", "[ ]", "[]()", "![]()", "<!-- image -->"}
CHUNK_SCHEMA_VERSION = "v2"
DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 200
CLAUSE_LIKE_PATTERN = re.compile(r"^(?:\d+[.)]|[A-Z][.)]|[IVXLCDM]+[.)])(?:\s+\S.*)?$")
MAX_STRUCTURAL_BLOCK_LENGTH = 120
EMBEDDING_SCHEMA_VERSION = "v1"
SUPPORTED_EMBEDDING_PROVIDER = "sentence-transformers"
DEFAULT_EMBEDDING_DIR = "data/processed/embeddings"


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

    embedding_parser = subparsers.add_parser("generate-embeddings")
    embedding_parser.add_argument("--chunk-dir", required=True)
    embedding_parser.add_argument("--embedding-dir", default=DEFAULT_EMBEDDING_DIR)
    embedding_parser.add_argument("--manifest-path", required=True)
    embedding_parser.add_argument("--glob", default="*.chunks.json")
    embedding_parser.add_argument("--overwrite", type=parse_bool, default=False)
    embedding_parser.add_argument("--fail-fast", type=parse_bool, default=False)
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


def validate_embedding_settings(settings: Settings) -> Settings:
    """Validate embedding configuration for offline artifact generation."""

    if settings.embedding_provider != SUPPORTED_EMBEDDING_PROVIDER:
        raise RuntimeError(
            "EMBEDDING_PROVIDER must be sentence-transformers for offline embedding generation."
        )
    if not settings.embedding_model.strip():
        raise RuntimeError("EMBEDDING_MODEL must not be blank for embedding generation.")
    return settings


def embedding_backend_is_available(settings: Settings) -> bool:
    """Return whether the configured embedding backend is importable."""

    if settings.embedding_provider != SUPPORTED_EMBEDDING_PROVIDER:
        return False
    return importlib.util.find_spec("sentence_transformers") is not None


def ensure_embedding_backend_available(settings: Settings) -> None:
    """Fail loudly when the configured embedding backend is unavailable."""

    if not embedding_backend_is_available(settings):
        raise RuntimeError(
            "Sentence Transformers is not installed. Install project dependencies "
            "before running embedding generation."
        )


@lru_cache(maxsize=4)
def load_sentence_transformer(model_name: str):
    """Return a cached SentenceTransformer instance for deterministic reuse."""

    sentence_transformers = importlib.import_module("sentence_transformers")
    return sentence_transformers.SentenceTransformer(model_name)


def generate_embedding_vector(text: str, settings: Settings) -> list[float]:
    """Generate one embedding vector for chunk text."""

    if settings.embedding_provider != SUPPORTED_EMBEDDING_PROVIDER:
        raise RuntimeError("Unsupported embedding provider for local embedding generation.")

    model = load_sentence_transformer(settings.embedding_model)
    vector = model.encode([text], normalize_embeddings=True)[0]
    return [float(value) for value in vector]


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


def build_embedding_payload(chunk_record: ChunkRecord) -> VectorPayload:
    """Build the explicit later-indexing payload from one chunk record."""

    return VectorPayload(
        chunk_id=chunk_record.chunk_id,
        source_pdf_id=chunk_record.source_pdf_id,
        chunk_schema_version=chunk_record.chunk_schema_version,
        chunk_index=chunk_record.chunk_index,
        document_name=chunk_record.document_name,
        document_version=chunk_record.document_version,
        section=chunk_record.section,
        section_path=chunk_record.section_path,
        text=chunk_record.text,
    )


def build_embedding_bundle(
    *,
    chunk_bundle: ChunkBundle,
    embedding_artifact_path: Path,
    settings: Settings,
) -> EmbeddingBundle:
    """Build a deterministic embedding bundle from one chunk bundle."""

    embedding_records: list[EmbeddingRecord] = []

    for chunk_record in chunk_bundle.chunks:
        vector = generate_embedding_vector(chunk_record.text, settings)
        embedding_records.append(
            EmbeddingRecord(
                chunk_id=chunk_record.chunk_id,
                source_pdf_id=chunk_record.source_pdf_id,
                chunk_schema_version=chunk_record.chunk_schema_version,
                embedding_provider=settings.embedding_provider,
                embedding_model=settings.embedding_model,
                vector_dimension=len(vector),
                vector=vector,
                payload=build_embedding_payload(chunk_record),
            )
        )

    if not embedding_records:
        raise RuntimeError("No chunk records were available for embedding generation.")

    return EmbeddingBundle(
        source_pdf_id=chunk_bundle.source_pdf_id,
        document_name=chunk_bundle.document_name,
        document_version=chunk_bundle.document_version,
        source_chunk_artifact_path=chunk_bundle.chunk_artifact_path,
        embedding_artifact_path=str(embedding_artifact_path),
        embedding_schema_version=EMBEDDING_SCHEMA_VERSION,
        chunk_schema_version=chunk_bundle.chunk_schema_version,
        embedding_provider=settings.embedding_provider,
        embedding_model=settings.embedding_model,
        vector_dimension=embedding_records[0].vector_dimension,
        embeddings=embedding_records,
    )


def write_embedding_bundle(
    embedding_bundle: EmbeddingBundle,
    embedding_artifact_path: Path,
) -> None:
    """Persist a deterministic embedding bundle to JSON."""

    embedding_artifact_path.parent.mkdir(parents=True, exist_ok=True)
    embedding_artifact_path.write_text(
        embedding_bundle.model_dump_json(indent=2),
        encoding="utf-8",
    )


def build_embedding_generation_record(
    *,
    chunk_bundle: ChunkBundle,
    embedding_artifact_path: Path,
    settings: Settings,
    generation_status: str,
    error_message: str | None = None,
) -> EmbeddingGenerationRecord:
    """Build one manifest record for embedding generation."""

    return EmbeddingGenerationRecord(
        source_pdf_id=chunk_bundle.source_pdf_id,
        source_chunk_artifact_path=chunk_bundle.chunk_artifact_path,
        embedding_artifact_path=str(embedding_artifact_path),
        embedding_provider=settings.embedding_provider,
        embedding_model=settings.embedding_model,
        generation_status=generation_status,
        error_message=error_message,
        generated_at=datetime.now(UTC),
    )


def build_failed_embedding_record_from_artifact_path(
    *,
    chunk_artifact_path: Path,
    embedding_artifact_path: Path,
    settings: Settings,
    error_message: str,
) -> EmbeddingGenerationRecord:
    """Build a failed embedding manifest record without a valid chunk bundle."""

    source_pdf_id = chunk_artifact_path.name.removesuffix(".chunks.json")
    return EmbeddingGenerationRecord(
        source_pdf_id=source_pdf_id,
        source_chunk_artifact_path=str(chunk_artifact_path),
        embedding_artifact_path=str(embedding_artifact_path),
        embedding_provider=settings.embedding_provider,
        embedding_model=settings.embedding_model,
        generation_status="failed",
        error_message=error_message,
        generated_at=datetime.now(UTC),
    )


def append_embedding_manifest_record(
    manifest_path: Path,
    record: EmbeddingGenerationRecord,
) -> None:
    """Append one JSONL embedding manifest record."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as manifest_file:
        manifest_file.write(record.model_dump_json())
        manifest_file.write("\n")


def iter_chunk_artifacts(chunk_dir: Path, glob_pattern: str) -> list[Path]:
    """Return sorted matching chunk artifacts under the configured directory."""

    return sorted(path for path in chunk_dir.glob(glob_pattern) if path.is_file())


def load_chunk_bundle(chunk_artifact_path: Path) -> ChunkBundle:
    """Load one persisted chunk bundle."""

    return ChunkBundle.model_validate_json(chunk_artifact_path.read_text(encoding="utf-8"))


def generate_embeddings_for_chunk_bundle(
    *,
    chunk_artifact_path: Path,
    embedding_dir: Path,
    settings: Settings,
    overwrite: bool,
) -> EmbeddingGenerationRecord:
    """Generate and persist embeddings for one chunk bundle artifact."""

    chunk_bundle = load_chunk_bundle(chunk_artifact_path)
    embedding_artifact_path = embedding_dir / f"{chunk_bundle.source_pdf_id}.embeddings.json"

    if not overwrite and embedding_artifact_path.exists():
        return build_embedding_generation_record(
            chunk_bundle=chunk_bundle,
            embedding_artifact_path=embedding_artifact_path,
            settings=settings,
            generation_status="skipped",
        )

    embedding_bundle = build_embedding_bundle(
        chunk_bundle=chunk_bundle,
        embedding_artifact_path=embedding_artifact_path,
        settings=settings,
    )
    write_embedding_bundle(embedding_bundle, embedding_artifact_path)
    return build_embedding_generation_record(
        chunk_bundle=chunk_bundle,
        embedding_artifact_path=embedding_artifact_path,
        settings=settings,
        generation_status="succeeded",
    )


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


def run_embedding_generation(args: argparse.Namespace) -> int:
    """Execute the offline embedding generation flow."""

    chunk_dir = Path(args.chunk_dir)
    embedding_dir = Path(args.embedding_dir)
    manifest_path = Path(args.manifest_path)

    if not chunk_dir.exists() or not chunk_dir.is_dir():
        print(f"Chunk directory does not exist: {chunk_dir}", file=sys.stderr)
        return 2

    settings = validate_embedding_settings(get_settings())
    ensure_embedding_backend_available(settings)

    chunk_artifacts = iter_chunk_artifacts(chunk_dir, args.glob)
    if not chunk_artifacts:
        print(
            f"No chunk artifacts matched glob '{args.glob}' in chunk directory: {chunk_dir}",
            file=sys.stderr,
        )
        return 2

    encountered_failures = False

    for chunk_artifact_path in chunk_artifacts:
        embedding_artifact_path = embedding_dir / (
            f"{chunk_artifact_path.name.removesuffix('.chunks.json')}.embeddings.json"
        )
        try:
            record = generate_embeddings_for_chunk_bundle(
                chunk_artifact_path=chunk_artifact_path,
                embedding_dir=embedding_dir,
                settings=settings,
                overwrite=args.overwrite,
            )
        except Exception as exc:
            encountered_failures = True
            try:
                chunk_bundle = load_chunk_bundle(chunk_artifact_path)
                embedding_artifact_path = (
                    embedding_dir / f"{chunk_bundle.source_pdf_id}.embeddings.json"
                )
                remove_artifact_if_exists(embedding_artifact_path)
                record = build_embedding_generation_record(
                    chunk_bundle=chunk_bundle,
                    embedding_artifact_path=embedding_artifact_path,
                    settings=settings,
                    generation_status="failed",
                    error_message=str(exc),
                )
            except Exception as load_exc:
                remove_artifact_if_exists(embedding_artifact_path)
                record = build_failed_embedding_record_from_artifact_path(
                    chunk_artifact_path=chunk_artifact_path,
                    embedding_artifact_path=embedding_artifact_path,
                    settings=settings,
                    error_message=f"{exc}; chunk artifact load failed: {load_exc}",
                )

        append_embedding_manifest_record(manifest_path, record)

        if record.generation_status == "failed":
            print(
                f"Failed to generate embeddings for {chunk_artifact_path.name}: "
                f"{record.error_message}",
                file=sys.stderr,
            )
            if args.fail_fast:
                return 1

    return 0 if not (encountered_failures and args.fail_fast) else 1


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint for the current offline ingestion and embedding pipeline."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "ingest-pdfs":
            return run_ingestion(args)
        if args.command == "generate-embeddings":
            return run_embedding_generation(args)
        parser.error(f"Unsupported command: {args.command}")
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
