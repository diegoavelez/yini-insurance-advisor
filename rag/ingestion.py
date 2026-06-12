"""Offline PDF ingestion CLI for the current Phase 2 and early Phase 3 slices."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import logging
import re
import subprocess
import sys
import time
import unicodedata
import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path

from contracts import (
    AdvisorDraftResponse,
    ChunkBundle,
    ChunkRecord,
    Citation,
    DocumentaryBasisItem,
    DocumentMetadataOverlayEntry,
    DocumentMetadataOverlaySet,
    DocumentRetrievalResult,
    EmbeddingBundle,
    EmbeddingGenerationRecord,
    EmbeddingIndexingRecord,
    EmbeddingRecord,
    GroundedAnswerResult,
    GroundingVerification,
    ProcessedDocument,
    RetrievalQuery,
    RetrievedChunk,
    TermEquivalenceSet,
    VectorPayload,
)
from core.config import Settings, get_settings, validate_startup_settings
from core.logging import configure_logging
from core.prompt_guardrails import detect_prompt_injection_signals
from core.query_scope import classify_query_scope
from ops.observability import (
    generate_request_id,
    log_event,
    log_startup_diagnostics,
    log_timed_event,
)

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
DEFAULT_QDRANT_INDEXING_MANIFEST = "data/processed/qdrant-indexing-manifest.jsonl"
DEFAULT_TERM_EQUIVALENCE_PATH = "ops/term-equivalences.json"
DEFAULT_QDRANT_MAX_RETRIES = 3
DEFAULT_QDRANT_RETRY_BACKOFF_SECONDS = 0.25
DEFAULT_DOCLING_STARTUP_TIMEOUT_SECONDS = 300.0
QDRANT_POINT_ID_NAMESPACE = uuid.UUID("8c39ce79-53d7-47e5-baad-95c5f1548599")
MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE = 2
ADVISOR_REVIEW_NOTICE = "This response is a draft for advisor review."
RAG_LOGGER = logging.getLogger("yini.rag")


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


def parse_positive_float(value: str) -> float:
    """Parse a strictly positive floating-point CLI value."""

    parsed_value = float(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("expected a float > 0")
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
    ingest_parser.add_argument("--metadata-overlay-path", default=None)
    ingest_parser.add_argument("--glob", default="*.pdf")
    ingest_parser.add_argument("--overwrite", type=parse_bool, default=False)
    ingest_parser.add_argument("--fail-fast", type=parse_bool, default=False)
    ingest_parser.add_argument("--chunk-size", type=parse_positive_int, default=DEFAULT_CHUNK_SIZE)
    ingest_parser.add_argument(
        "--chunk-overlap",
        type=parse_non_negative_int,
        default=DEFAULT_CHUNK_OVERLAP,
    )
    ingest_parser.add_argument(
        "--pdf-conversion-backend",
        choices=("docling", "auto", "pdfium"),
        default="docling",
    )
    ingest_parser.add_argument(
        "--docling-startup-timeout-seconds",
        type=parse_positive_float,
        default=DEFAULT_DOCLING_STARTUP_TIMEOUT_SECONDS,
    )

    warmup_parser = subparsers.add_parser("warmup-docling-assets")
    warmup_parser.add_argument("--sample-pdf", required=True)
    warmup_parser.add_argument(
        "--docling-startup-timeout-seconds",
        type=parse_positive_float,
        default=DEFAULT_DOCLING_STARTUP_TIMEOUT_SECONDS,
    )

    embedding_parser = subparsers.add_parser("generate-embeddings")
    embedding_parser.add_argument("--chunk-dir", required=True)
    embedding_parser.add_argument("--embedding-dir", default=DEFAULT_EMBEDDING_DIR)
    embedding_parser.add_argument("--manifest-path", required=True)
    embedding_parser.add_argument("--glob", default="*.chunks.json")
    embedding_parser.add_argument("--overwrite", type=parse_bool, default=False)
    embedding_parser.add_argument("--fail-fast", type=parse_bool, default=False)

    qdrant_parser = subparsers.add_parser("index-embeddings")
    qdrant_parser.add_argument("--embedding-dir", default=DEFAULT_EMBEDDING_DIR)
    qdrant_parser.add_argument("--manifest-path", default=DEFAULT_QDRANT_INDEXING_MANIFEST)
    qdrant_parser.add_argument("--glob", default="*.embeddings.json")
    qdrant_parser.add_argument("--fail-fast", type=parse_bool, default=False)
    qdrant_parser.add_argument(
        "--max-retries",
        type=parse_non_negative_int,
        default=DEFAULT_QDRANT_MAX_RETRIES,
    )
    qdrant_parser.add_argument(
        "--retry-backoff-seconds",
        type=float,
        default=DEFAULT_QDRANT_RETRY_BACKOFF_SECONDS,
    )

    retrieval_parser = subparsers.add_parser("retrieve-chunks")
    retrieval_parser.add_argument("--query", required=True)
    retrieval_parser.add_argument("--top-k", type=parse_positive_int, default=None)
    retrieval_parser.add_argument("--document-type", default=None)
    retrieval_parser.add_argument("--product", default=None)
    retrieval_parser.add_argument("--document-name", default=None)
    retrieval_parser.add_argument("--version", default=None)

    answer_parser = subparsers.add_parser("answer-query")
    answer_parser.add_argument("--query", required=True)
    answer_parser.add_argument("--top-k", type=parse_positive_int, default=None)
    answer_parser.add_argument("--document-type", default=None)
    answer_parser.add_argument("--product", default=None)
    answer_parser.add_argument("--document-name", default=None)
    answer_parser.add_argument("--version", default=None)
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


def pdfium_backend_is_available() -> bool:
    """Return whether the PDFium fallback backend is importable."""

    return importlib.util.find_spec("pypdfium2") is not None


def ensure_pdf_conversion_backend_available(*, backend: str) -> None:
    """Fail loudly when no supported local PDF conversion backend is available."""

    if backend == "docling":
        if docling_is_available():
            return
        raise RuntimeError(
            "Docling is not installed. Install project dependencies before running "
            "the ingestion CLI with the Docling backend."
        )
    if backend == "pdfium":
        if pdfium_backend_is_available():
            return
        raise RuntimeError(
            "pypdfium2 is not installed. Install project dependencies before running "
            "the ingestion CLI with the PDFium backend."
        )
    if docling_is_available() or pdfium_backend_is_available():
        return
    raise RuntimeError(
        "No supported PDF conversion backend is installed. Install Docling or "
        "pypdfium2 before running the ingestion CLI."
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


def qdrant_backend_is_available() -> bool:
    """Return whether the Qdrant client is importable."""

    return importlib.util.find_spec("qdrant_client") is not None


def ensure_qdrant_backend_available() -> None:
    """Fail loudly when the Qdrant client is unavailable."""

    if not qdrant_backend_is_available():
        raise RuntimeError(
            "qdrant-client is not installed. Install project dependencies before "
            "running Qdrant indexing."
        )


def groq_backend_is_available() -> bool:
    """Return whether the Groq client is importable."""

    return importlib.util.find_spec("groq") is not None


def call_with_optional_request_id(function, *args, request_id: str | None = None, **kwargs):
    """Call a seam with request_id when supported, otherwise retry without it."""

    if request_id is None:
        return function(*args, **kwargs)
    try:
        return function(*args, request_id=request_id, **kwargs)
    except TypeError as exc:
        if "request_id" not in str(exc):
            raise
        return function(*args, **kwargs)


def ensure_groq_backend_available() -> None:
    """Fail loudly when the Groq client is unavailable."""

    if not groq_backend_is_available():
        raise RuntimeError(
            "groq is not installed. Install project dependencies before running "
            "grounded answer generation."
        )


def create_groq_client(settings: Settings):
    """Create a configured Groq client from validated settings."""

    groq_module = importlib.import_module("groq")
    return groq_module.Groq(api_key=settings.groq_api_key.get_secret_value())


def get_qdrant_models():
    """Return qdrant-client models lazily to keep import costs scoped."""

    qdrant_http = importlib.import_module("qdrant_client.http.models")
    return qdrant_http


def create_qdrant_client(settings: Settings):
    """Create a configured Qdrant client from validated settings."""

    qdrant_client = importlib.import_module("qdrant_client")
    return qdrant_client.QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key.get_secret_value() if settings.qdrant_api_key else None,
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


def generate_grounded_completion(prompt: str, settings: Settings) -> str:
    """Generate grounded completion text through Groq."""

    client = create_groq_client(settings)
    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an internal insurance assistant. Answer only from the "
                    "provided evidence. If evidence is insufficient, say so explicitly."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    message = response.choices[0].message
    content = getattr(message, "content", None)
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("Groq did not return grounded answer content.")
    return content.strip()


def convert_pdf_to_markdown_with_docling(
    source_pdf_path: Path,
    *,
    startup_timeout_seconds: float,
) -> str:
    """Convert one PDF to markdown through Docling in an isolated subprocess."""

    script = """
from pathlib import Path
import sys
from docling.document_converter import DocumentConverter

source_pdf_path = Path(sys.argv[1])
converter = DocumentConverter()
result = converter.convert(str(source_pdf_path))
document = getattr(result, "document", None)
if document is not None and hasattr(document, "export_to_markdown"):
    markdown = document.export_to_markdown()
else:
    markdown = getattr(result, "markdown", None)
if not isinstance(markdown, str) or not markdown.strip():
    raise RuntimeError("Docling conversion result did not expose markdown output.")
sys.stdout.write(markdown)
"""
    completed = subprocess.run(
        [sys.executable, "-c", script, str(source_pdf_path)],
        capture_output=True,
        text=True,
        timeout=startup_timeout_seconds,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.strip()
            or "Docling conversion failed without a detailed error message."
        )
    markdown = completed.stdout
    if not markdown.strip():
        raise RuntimeError("Docling conversion produced empty markdown output.")
    return markdown


def convert_pdf_to_markdown_with_pdfium(source_pdf_path: Path) -> str:
    """Convert one PDF into simple markdown through the PDFium text fallback."""

    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(source_pdf_path))
    markdown_sections = [f"# {source_pdf_path.stem}"]

    for page_index in range(len(pdf)):
        page = pdf[page_index]
        text_page = page.get_textpage()
        page_text = text_page.get_text_range().strip()
        if not page_text:
            continue
        markdown_sections.extend(
            [
                "",
                f"## Page {page_index + 1}",
                "",
                page_text,
            ]
        )

    markdown = "\n".join(markdown_sections).strip()
    if not markdown:
        raise RuntimeError("PDFium fallback conversion produced empty markdown output.")
    return f"{markdown}\n"


def convert_pdf_to_markdown(source_pdf_path: Path) -> str:
    """Convert one PDF to markdown using Docling first and PDFium as fallback."""

    return convert_pdf_to_markdown_with_backend(
        source_pdf_path,
        backend="docling",
        docling_startup_timeout_seconds=DEFAULT_DOCLING_STARTUP_TIMEOUT_SECONDS,
    )


def convert_pdf_to_markdown_with_backend(
    source_pdf_path: Path,
    *,
    backend: str,
    docling_startup_timeout_seconds: float,
) -> str:
    """Convert one PDF to markdown using the selected backend policy."""

    fallback_error: Exception | None = None
    if backend in {"docling", "auto"} and docling_is_available():
        try:
            return convert_pdf_to_markdown_with_docling(
                source_pdf_path,
                startup_timeout_seconds=docling_startup_timeout_seconds,
            )
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            fallback_error = exc

    if backend == "docling" and fallback_error is not None:
        raise RuntimeError(
            "Docling conversion did not complete under the configured local timeout."
        ) from fallback_error

    if backend in {"pdfium", "auto"} and pdfium_backend_is_available():
        return convert_pdf_to_markdown_with_pdfium(source_pdf_path)

    if fallback_error is not None:
        raise RuntimeError(
            "Docling conversion did not complete and no PDFium fallback backend is available."
        ) from fallback_error
    ensure_pdf_conversion_backend_available(backend=backend)
    raise RuntimeError("No PDF conversion backend produced markdown output.")


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


def load_document_metadata_overlays(
    metadata_overlay_path: Path | None,
) -> dict[str, DocumentMetadataOverlayEntry]:
    """Load an optional operator-curated document metadata overlay set."""

    if metadata_overlay_path is None:
        return {}
    overlay_set = DocumentMetadataOverlaySet.model_validate_json(
        metadata_overlay_path.read_text(encoding="utf-8")
    )
    return overlay_set.documents


def normalize_equivalence_text(value: str) -> str:
    """Normalize one term-equivalence key for stable phrase matching."""

    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.strip().lower().split())


def load_term_equivalences(term_equivalence_path: Path | None = None) -> TermEquivalenceSet:
    """Load optional operator-curated term equivalences."""

    resolved_path = term_equivalence_path or Path(DEFAULT_TERM_EQUIVALENCE_PATH)
    if not resolved_path.exists():
        return TermEquivalenceSet()
    return TermEquivalenceSet.model_validate_json(resolved_path.read_text(encoding="utf-8"))


def query_contains_equivalent_phrase(query: str, phrase: str) -> bool:
    """Return whether a normalized phrase appears in the normalized query."""

    normalized_phrase = normalize_equivalence_text(phrase)
    if not normalized_phrase:
        return False
    pattern = rf"(?<!\w){re.escape(normalized_phrase)}(?!\w)"
    return re.search(pattern, normalize_equivalence_text(query)) is not None


def augment_query_with_term_equivalences(query: str, term_equivalences: TermEquivalenceSet) -> str:
    """Append operator-curated canonical terms when aliases appear in the query."""

    appended_terms: list[str] = []
    for canonical_term, aliases in term_equivalences.query_aliases.items():
        if query_contains_equivalent_phrase(query, canonical_term):
            continue
        if any(query_contains_equivalent_phrase(query, alias) for alias in aliases):
            appended_terms.append(canonical_term)

    if not appended_terms:
        return query
    return f"{query}\n\nTérminos equivalentes: {', '.join(appended_terms)}"


def canonicalize_filter_value(
    *,
    field_name: str,
    value: str | None,
    term_equivalences: TermEquivalenceSet,
) -> str | None:
    """Map one filter value to its canonical operator-curated equivalent."""

    if value is None:
        return None

    normalized_value = normalize_equivalence_text(value)
    field_aliases = term_equivalences.filter_aliases.get(field_name, {})
    for canonical_value, aliases in field_aliases.items():
        if normalized_value == normalize_equivalence_text(canonical_value):
            return canonical_value
        if normalized_value in {normalize_equivalence_text(alias) for alias in aliases}:
            return canonical_value
    return value


def normalize_retrieval_query_with_term_equivalences(
    retrieval_query: RetrievalQuery,
    *,
    term_equivalences: TermEquivalenceSet,
) -> RetrievalQuery:
    """Apply operator-curated term equivalences to query text and filters."""

    return RetrievalQuery(
        query=augment_query_with_term_equivalences(retrieval_query.query, term_equivalences),
        top_k=retrieval_query.top_k,
        filters={
            "document_type": canonicalize_filter_value(
                field_name="document_type",
                value=retrieval_query.filters.document_type,
                term_equivalences=term_equivalences,
            ),
            "product": canonicalize_filter_value(
                field_name="product",
                value=retrieval_query.filters.product,
                term_equivalences=term_equivalences,
            ),
            "document_name": retrieval_query.filters.document_name,
            "version": retrieval_query.filters.version,
        },
    )


def build_processed_document(
    *,
    source_pdf_id: str,
    source_pdf_path: Path,
    source_pdf_relative_path: Path,
    markdown_output_path: Path,
    cleaned_markdown_output_path: Path,
    processed_output_path: Path,
    ingestion_status: str,
    document_name: str | None = None,
    document_version: str | None = None,
    document_type: str | None = None,
    product: str | None = None,
    error_message: str | None = None,
) -> ProcessedDocument:
    """Build one deterministic processed-document record."""

    return ProcessedDocument(
        source_pdf_id=source_pdf_id,
        source_pdf_path=str(source_pdf_path),
        source_pdf_relative_path=source_pdf_relative_path.as_posix(),
        markdown_output_path=str(markdown_output_path),
        cleaned_markdown_output_path=str(cleaned_markdown_output_path),
        processed_output_path=str(processed_output_path),
        document_name=document_name or source_pdf_id,
        document_version=document_version,
        document_type=document_type,
        product=product,
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

    return sorted(path for path in input_dir.rglob(glob_pattern) if path.is_file())


def slugify_path_component(value: str) -> str:
    """Return a deterministic ASCII slug for one source-path component."""

    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return slug or "document"


def derive_source_pdf_id(*, input_dir: Path, source_pdf_path: Path) -> str:
    """Derive a collision-safe document id from the relative source path."""

    relative_path = source_pdf_path.relative_to(input_dir)
    components = [*relative_path.parts[:-1], relative_path.stem]
    return "__".join(slugify_path_component(component) for component in components)


def build_ingestion_artifact_paths(
    *,
    source_pdf_id: str,
    markdown_dir: Path,
    processed_dir: Path,
) -> tuple[Path, Path, Path, Path]:
    """Build deterministic artifact paths for one source document id."""

    markdown_output_path = markdown_dir / f"{source_pdf_id}.md"
    cleaned_markdown_output_path = processed_dir / f"{source_pdf_id}.cleaned.md"
    processed_output_path = processed_dir / f"{source_pdf_id}.json"
    chunk_artifact_path = processed_dir / "chunks" / f"{source_pdf_id}.chunks.json"
    return (
        markdown_output_path,
        cleaned_markdown_output_path,
        processed_output_path,
        chunk_artifact_path,
    )


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
    document_type: str | None = None,
    product: str | None = None,
    source_pdf_path: Path,
    source_pdf_relative_path: Path,
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
                document_type=document_type,
                product=product,
                source_pdf_path=str(source_pdf_path),
                source_pdf_relative_path=source_pdf_relative_path.as_posix(),
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
        document_type=processed_document.document_type,
        product=processed_document.product,
        source_pdf_path=Path(processed_document.source_pdf_path),
        source_pdf_relative_path=Path(processed_document.source_pdf_relative_path),
        cleaned_markdown_output_path=Path(processed_document.cleaned_markdown_output_path),
        cleaned_markdown_text=cleaned_markdown_text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return ChunkBundle(
        source_pdf_id=processed_document.source_pdf_id,
        document_name=processed_document.document_name,
        document_version=processed_document.document_version,
        document_type=processed_document.document_type,
        product=processed_document.product,
        source_pdf_path=processed_document.source_pdf_path,
        source_pdf_relative_path=processed_document.source_pdf_relative_path,
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
        source_pdf_relative_path=chunk_record.source_pdf_relative_path,
        chunk_schema_version=chunk_record.chunk_schema_version,
        chunk_index=chunk_record.chunk_index,
        document_name=chunk_record.document_name,
        document_version=chunk_record.document_version,
        document_type=chunk_record.document_type,
        product=chunk_record.product,
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
        document_type=chunk_bundle.document_type,
        product=chunk_bundle.product,
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


def append_indexing_manifest_record(
    manifest_path: Path,
    record: EmbeddingIndexingRecord,
) -> None:
    """Append one JSONL indexing manifest record."""

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


def load_embedding_bundle(embedding_artifact_path: Path) -> EmbeddingBundle:
    """Load one persisted embedding bundle."""

    return EmbeddingBundle.model_validate_json(embedding_artifact_path.read_text(encoding="utf-8"))


def iter_embedding_artifacts(embedding_dir: Path, glob_pattern: str) -> list[Path]:
    """Return sorted matching embedding artifacts under the configured directory."""

    return sorted(path for path in embedding_dir.glob(glob_pattern) if path.is_file())


def build_qdrant_point_id(embedding_record: EmbeddingRecord) -> str:
    """Return the deterministic Qdrant point id for one embedding record."""

    return str(uuid.uuid5(QDRANT_POINT_ID_NAMESPACE, embedding_record.chunk_id))


def build_qdrant_point_payload(embedding_record: EmbeddingRecord) -> dict[str, object]:
    """Map a typed embedding record into a Qdrant payload."""

    return {
        "chunk_id": embedding_record.chunk_id,
        "source_pdf_id": embedding_record.source_pdf_id,
        "source_pdf_relative_path": embedding_record.payload.source_pdf_relative_path,
        "chunk_schema_version": embedding_record.chunk_schema_version,
        "embedding_provider": embedding_record.embedding_provider,
        "embedding_model": embedding_record.embedding_model,
        "document_name": embedding_record.payload.document_name,
        "document_version": embedding_record.payload.document_version,
        "document_type": embedding_record.payload.document_type,
        "product": embedding_record.payload.product,
        "chunk_index": embedding_record.payload.chunk_index,
        "section": embedding_record.payload.section,
        "section_path": embedding_record.payload.section_path,
        "text": embedding_record.payload.text,
    }


def build_qdrant_query_filter(filters: object) -> object | None:
    """Map typed retrieval filters into a Qdrant filter object."""

    filter_mappings = {
        "document_type": "document_type",
        "product": "product",
        "document_name": "document_name",
        "version": "document_version",
    }
    filter_values = {
        field_name: getattr(filters, field_name, None) for field_name in filter_mappings
    }
    if all(value is None for value in filter_values.values()):
        return None

    conditions: list[object] = []
    qdrant_models = get_qdrant_models()

    for field_name, payload_key in filter_mappings.items():
        value = filter_values[field_name]
        if value is None:
            continue
        conditions.append(
            qdrant_models.FieldCondition(
                key=payload_key,
                match=qdrant_models.MatchValue(value=value),
            )
        )

    if not conditions:
        return None

    return qdrant_models.Filter(must=conditions)


def build_qdrant_points(embedding_bundle: EmbeddingBundle) -> list[object]:
    """Map one embedding bundle into deterministic Qdrant points."""

    qdrant_models = get_qdrant_models()
    return [
        qdrant_models.PointStruct(
            id=build_qdrant_point_id(embedding_record),
            vector=embedding_record.vector,
            payload=build_qdrant_point_payload(embedding_record),
        )
        for embedding_record in embedding_bundle.embeddings
    ]


def map_search_hit_to_retrieved_chunk(hit: object) -> RetrievedChunk:
    """Map one Qdrant search hit into a typed retrieval result."""

    payload = getattr(hit, "payload", None)
    if not isinstance(payload, dict):
        raise RuntimeError("Qdrant search hit payload is missing or invalid.")

    chunk_id = payload.get("chunk_id")
    text = payload.get("text")
    document_name = payload.get("document_name")
    if (
        not isinstance(chunk_id, str)
        or not isinstance(text, str)
        or not isinstance(document_name, str)
    ):
        raise RuntimeError("Qdrant search hit payload is missing required retrieval fields.")

    score = getattr(hit, "score", None)
    if score is None:
        score = 0.0

    source_pdf_id = payload.get("source_pdf_id")
    if not isinstance(source_pdf_id, str):
        source_pdf_id = None
    source_pdf_relative_path = payload.get("source_pdf_relative_path")
    if not isinstance(source_pdf_relative_path, str):
        source_pdf_relative_path = None
    chunk_schema_version = payload.get("chunk_schema_version")
    if not isinstance(chunk_schema_version, str):
        chunk_schema_version = None
    chunk_index = payload.get("chunk_index")
    if not isinstance(chunk_index, int):
        chunk_index = None
    document_version = payload.get("document_version")
    if not isinstance(document_version, str):
        document_version = None
    document_type = payload.get("document_type")
    if not isinstance(document_type, str):
        document_type = None
    product = payload.get("product")
    if not isinstance(product, str):
        product = None
    page = payload.get("page")
    if not isinstance(page, int):
        page = None
    section = payload.get("section")
    if not isinstance(section, str):
        section = None
    section_path = payload.get("section_path")
    if not isinstance(section_path, list) or not all(
        isinstance(value, str) for value in section_path
    ):
        section_path = []
    clause_id = payload.get("clause_id")
    if not isinstance(clause_id, str):
        clause_id = None

    return RetrievedChunk(
        chunk_id=chunk_id,
        source_pdf_id=source_pdf_id,
        source_pdf_relative_path=source_pdf_relative_path,
        chunk_schema_version=chunk_schema_version,
        chunk_index=chunk_index,
        text=text,
        document_name=document_name,
        document_version=document_version,
        document_type=document_type,
        product=product,
        page=page,
        section=section,
        section_path=section_path,
        clause_id=clause_id,
        score=float(score),
    )


def search_qdrant_chunks(
    *,
    client: object,
    settings: Settings,
    retrieval_query: RetrievalQuery,
    query_vector: list[float],
) -> list[object]:
    """Execute one Qdrant search for retrieval."""

    query_filter = build_qdrant_query_filter(retrieval_query.filters)
    if hasattr(client, "search"):
        return client.search(
            collection_name=settings.qdrant_collection,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=retrieval_query.top_k,
            with_payload=True,
        )
    if hasattr(client, "query_points"):
        response = client.query_points(
            collection_name=settings.qdrant_collection,
            query=query_vector,
            query_filter=query_filter,
            limit=retrieval_query.top_k,
            with_payload=True,
        )
        points = getattr(response, "points", None)
        if not isinstance(points, list):
            raise RuntimeError("Qdrant query_points response did not include ranked points.")
        return points
    raise RuntimeError("Installed Qdrant client does not expose a supported retrieval method.")


def retrieve_ranked_chunks(
    retrieval_query: RetrievalQuery,
    *,
    settings: Settings | None = None,
    client: object | None = None,
    request_id: str | None = None,
) -> DocumentRetrievalResult:
    """Retrieve ranked chunks from Qdrant using typed query contracts."""

    with log_timed_event(
        RAG_LOGGER,
        event_type="retrieval_execution",
        request_id=request_id,
        start_fields={
            "top_k": retrieval_query.top_k,
            "has_filters": bool(retrieval_query.filters),
        },
        success_fields_factory=lambda _duration_ms: {"result_count": len(result.chunks)},
    ):
        resolved_settings = validate_embedding_settings(
            validate_startup_settings(settings or get_settings(), require_qdrant=True)
        )
        normalized_retrieval_query = normalize_retrieval_query_with_term_equivalences(
            retrieval_query,
            term_equivalences=load_term_equivalences(),
        )
        ensure_qdrant_backend_available()
        resolved_client = client or create_qdrant_client(resolved_settings)
        query_vector = generate_embedding_vector(normalized_retrieval_query.query, resolved_settings)
        hits = search_qdrant_chunks(
            client=resolved_client,
            settings=resolved_settings,
            retrieval_query=normalized_retrieval_query,
            query_vector=query_vector,
        )
        result = DocumentRetrievalResult(
            chunks=[map_search_hit_to_retrieved_chunk(hit) for hit in hits]
        )
        return result


def build_grounded_prompt(
    *,
    query: str,
    retrieved_chunks: list[RetrievedChunk],
) -> str:
    """Build a deterministic grounded-answer prompt from retrieved evidence."""

    evidence_sections: list[str] = []
    for chunk in retrieved_chunks:
        evidence_sections.append(
            "\n".join(
                [
                    f"Chunk ID: {chunk.chunk_id}",
                    f"Document: {chunk.document_name}",
                    f"Section: {chunk.section or 'Unknown'}",
                    f"Text: {chunk.text}",
                ]
            )
        )

    evidence_block = "\n\n---\n\n".join(evidence_sections)
    return (
        "Answer the advisor's question using only the evidence below.\n"
        "If the evidence is insufficient, say that explicitly and do not invent details.\n\n"
        f"Question: {query}\n\n"
        f"Evidence:\n{evidence_block}"
    )


def build_citations_from_chunks(retrieved_chunks: list[RetrievedChunk]) -> list[Citation]:
    """Derive explicit citations from retrieved evidence."""

    citations: list[Citation] = []
    for chunk in retrieved_chunks:
        citations.append(
            Citation(
                document_name=chunk.document_name,
                source_pdf_relative_path=chunk.source_pdf_relative_path,
                document_type=chunk.document_type,
                product=chunk.product,
                chunk_id=chunk.chunk_id,
                page=chunk.page,
                section=chunk.section,
                clause_id=chunk.clause_id,
                quote=chunk.text[:280],
            )
        )
    return citations


def build_documentary_basis(retrieved_chunks: list[RetrievedChunk]) -> list[DocumentaryBasisItem]:
    """Map retrieved evidence into documentary basis items."""

    return [
        DocumentaryBasisItem(
            document_name=chunk.document_name,
            source_pdf_relative_path=chunk.source_pdf_relative_path,
            document_type=chunk.document_type,
            product=chunk.product,
            page=chunk.page,
            section=chunk.section,
            clause_id=chunk.clause_id,
            note=f"Derived from chunk {chunk.chunk_id}",
        )
        for chunk in retrieved_chunks
    ]


def assess_grounding(
    *,
    retrieved_chunks: list[RetrievedChunk],
    citations: list[Citation],
) -> GroundingVerification:
    """Build a simple typed grounding assessment from evidence availability."""

    if not retrieved_chunks:
        return GroundingVerification(
            supported=False,
            confidence="low",
            unsupported_claims=["No retrieval evidence was available."],
            missing_citations=["No citations available because retrieval returned no chunks."],
        )

    if len(retrieved_chunks) >= MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE and citations:
        return GroundingVerification(supported=True, confidence="high")

    return GroundingVerification(
        supported=True,
        confidence="medium",
        missing_citations=(
            [] if citations else ["No citations were derived from retrieved evidence."]
        ),
    )


def build_insufficient_evidence_response(
    *,
    query: str,
    retrieved_chunks: list[RetrievedChunk],
    limitation_note: str | None = None,
) -> GroundedAnswerResult:
    """Return a typed limited grounded response for insufficient evidence."""

    citations = build_citations_from_chunks(retrieved_chunks)
    verification = assess_grounding(retrieved_chunks=retrieved_chunks, citations=citations)
    limitations = [
        limitation_note or "Retrieved evidence is insufficient for a strong grounded answer."
    ]
    return GroundedAnswerResult(
        query=query,
        response=AdvisorDraftResponse(
            suggested_answer=(
                "I do not have enough grounded evidence in the retrieved documents to answer "
                "this confidently."
            ),
            documentary_basis=build_documentary_basis(retrieved_chunks),
            citations=citations,
            confidence="low",
            limitations=limitations,
            advisor_review_notice=ADVISOR_REVIEW_NOTICE,
        ),
        verification=verification,
    )


def build_unsupported_query_response(*, query: str) -> GroundedAnswerResult:
    """Return a typed conservative refusal for out-of-scope queries."""

    verification = GroundingVerification(
        supported=False,
        confidence="low",
        unsupported_claims=[
            "The query is outside the supported insurance-document scope for this assistant."
        ],
        missing_citations=["No citations are available for an out-of-scope refusal outcome."],
    )
    return GroundedAnswerResult(
        query=query,
        response=AdvisorDraftResponse(
            suggested_answer=(
                "I cannot answer that request within the supported insurance-document scope "
                "of this assistant."
            ),
            documentary_basis=[],
            citations=[],
            confidence="low",
            limitations=["This request is outside the supported insurance-document scope."],
            advisor_review_notice=ADVISOR_REVIEW_NOTICE,
        ),
        verification=verification,
    )


def build_prompt_injection_refusal_response(*, query: str) -> GroundedAnswerResult:
    """Return a typed conservative refusal for prompt-injection-like queries."""

    verification = GroundingVerification(
        supported=False,
        confidence="low",
        unsupported_claims=[
            (
                "The query included instructions that conflict with the assistant's "
                "grounded-use boundaries."
            )
        ],
        missing_citations=["No citations are available for a prompt-injection refusal outcome."],
    )
    return GroundedAnswerResult(
        query=query,
        response=AdvisorDraftResponse(
            suggested_answer=(
                "I cannot follow instructions that attempt to override the assistant's "
                "grounded-use rules or reveal hidden system behavior."
            ),
            documentary_basis=[],
            citations=[],
            confidence="low",
            limitations=[
                (
                    "This request triggered a prompt-injection guardrail and was refused "
                    "conservatively."
                )
            ],
            advisor_review_notice=ADVISOR_REVIEW_NOTICE,
        ),
        verification=verification,
    )


def build_missing_citation_guardrail_response(
    *,
    query: str,
    retrieved_chunks: list[RetrievedChunk],
) -> GroundedAnswerResult:
    """Return a typed guarded outcome for citationless answerable responses."""

    verification = GroundingVerification(
        supported=False,
        confidence="low",
        unsupported_claims=[
            "No traceable citations could be derived from the retrieved evidence."
        ],
        missing_citations=["At least one citation is required for an answerable response."],
    )
    return GroundedAnswerResult(
        query=query,
        response=AdvisorDraftResponse(
            suggested_answer=(
                "I cannot provide a grounded answer because the retrieved evidence did not "
                "produce traceable citations."
            ),
            documentary_basis=build_documentary_basis(retrieved_chunks),
            citations=[],
            confidence="low",
            limitations=[
                (
                    "At least one traceable citation is required before surfacing "
                    "an answerable response."
                )
            ],
            advisor_review_notice=ADVISOR_REVIEW_NOTICE,
        ),
        verification=verification,
    )


def generate_grounded_answer(
    retrieval_query: RetrievalQuery,
    *,
    settings: Settings | None = None,
    retrieval_result: DocumentRetrievalResult | None = None,
    completion_generator: callable | None = None,
    request_id: str | None = None,
) -> GroundedAnswerResult:
    """Generate the first typed grounded draft answer from retrieved evidence."""

    with log_timed_event(
        RAG_LOGGER,
        event_type="grounded_answer_execution",
        request_id=request_id,
        start_fields={"top_k": retrieval_query.top_k},
        success_fields_factory=lambda _duration_ms: {
            "confidence": result.response.confidence,
            "citation_count": len(result.response.citations),
            "limitation_count": len(result.response.limitations),
        },
    ):
        injection_decision = detect_prompt_injection_signals(retrieval_query.query)
        if injection_decision.triggered:
            log_event(
                RAG_LOGGER,
                event_type="prompt_injection_guardrail_triggered",
                request_id=request_id,
                guardrail_surface="grounded_answer_generation",
                triggered_signals=injection_decision.signals,
                refusal_reason=injection_decision.reason,
            )
            result = build_prompt_injection_refusal_response(query=retrieval_query.query)
            return result
        scope_decision = classify_query_scope(retrieval_query.query)
        if scope_decision.scope == "unsupported":
            log_event(
                RAG_LOGGER,
                event_type="query_scope_refusal",
                request_id=request_id,
                scope="unsupported",
                refusal_reason=scope_decision.reason,
            )
            result = build_unsupported_query_response(query=retrieval_query.query)
            return result
        resolved_settings = validate_startup_settings(
            settings or get_settings(),
            require_groq=True,
            require_qdrant=True,
        )
        validate_embedding_settings(resolved_settings)
        ensure_groq_backend_available()

        resolved_retrieval_result = retrieval_result or call_with_optional_request_id(
            retrieve_ranked_chunks,
            retrieval_query,
            settings=resolved_settings,
            request_id=request_id,
        )
        retrieved_chunks = resolved_retrieval_result.chunks
        if not retrieved_chunks:
            result = build_insufficient_evidence_response(
                query=retrieval_query.query,
                retrieved_chunks=retrieved_chunks,
            )
            return result
        if len(retrieved_chunks) < MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE:
            result = build_insufficient_evidence_response(
                query=retrieval_query.query,
                retrieved_chunks=retrieved_chunks,
                limitation_note=(
                    "Retrieved evidence is too limited to support a strong grounded answer."
                ),
            )
            return result

        citations = build_citations_from_chunks(retrieved_chunks)
        if not citations:
            log_event(
                RAG_LOGGER,
                event_type="citation_presence_guardrail_triggered",
                request_id=request_id,
                guardrail_surface="grounded_answer_generation",
                retrieved_chunk_count=len(retrieved_chunks),
                citation_count=0,
            )
            result = build_missing_citation_guardrail_response(
                query=retrieval_query.query,
                retrieved_chunks=retrieved_chunks,
            )
            return result
        prompt = build_grounded_prompt(
            query=retrieval_query.query,
            retrieved_chunks=retrieved_chunks,
        )
        completion_fn = completion_generator or generate_grounded_completion
        suggested_answer = completion_fn(prompt, resolved_settings)
        verification = assess_grounding(retrieved_chunks=retrieved_chunks, citations=citations)

        limitations: list[str] = []
        confidence = verification.confidence
        if confidence != "high":
            limitations.append(
                "Evidence is partial; advisor review is required before relying on this draft."
            )

        result = GroundedAnswerResult(
            query=retrieval_query.query,
            response=AdvisorDraftResponse(
                suggested_answer=suggested_answer,
                documentary_basis=build_documentary_basis(retrieved_chunks),
                citations=citations,
                confidence=confidence,
                limitations=limitations,
                advisor_review_notice=ADVISOR_REVIEW_NOTICE,
            ),
            verification=verification,
        )
        return result


def get_collection_vector_size(collection_info: object) -> int | None:
    """Extract collection vector size from a Qdrant collection descriptor."""

    config = getattr(collection_info, "config", None)
    params = getattr(config, "params", None)
    vectors = getattr(params, "vectors", None)
    if vectors is None:
        return None
    size = getattr(vectors, "size", None)
    if isinstance(size, int):
        return size
    if isinstance(vectors, dict):
        first_vector = next(iter(vectors.values()), None)
        nested_size = getattr(first_vector, "size", None)
        if isinstance(nested_size, int):
            return nested_size
    return None


def ensure_qdrant_collection(client: object, settings: Settings, vector_size: int) -> None:
    """Create or validate the target Qdrant collection."""

    qdrant_models = get_qdrant_models()

    try:
        collection_info = client.get_collection(settings.qdrant_collection)
    except Exception:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=qdrant_models.VectorParams(
                size=vector_size,
                distance=qdrant_models.Distance.COSINE,
            ),
        )
        collection_info = client.get_collection(settings.qdrant_collection)

    configured_size = get_collection_vector_size(collection_info)
    if configured_size != vector_size:
        raise RuntimeError(
            "Configured Qdrant collection is incompatible with the embedding vector dimension."
        )


def build_indexing_record(
    *,
    embedding_bundle: EmbeddingBundle,
    settings: Settings,
    indexing_status: str,
    indexed_point_count: int,
    error_message: str | None = None,
) -> EmbeddingIndexingRecord:
    """Build one indexing manifest record."""

    return EmbeddingIndexingRecord(
        source_pdf_id=embedding_bundle.source_pdf_id,
        embedding_artifact_path=embedding_bundle.embedding_artifact_path,
        qdrant_collection=settings.qdrant_collection,
        indexed_point_count=indexed_point_count,
        indexing_status=indexing_status,
        error_message=error_message,
        indexed_at=datetime.now(UTC),
    )


def build_failed_indexing_record_from_artifact_path(
    *,
    embedding_artifact_path: Path,
    settings: Settings,
    error_message: str,
) -> EmbeddingIndexingRecord:
    """Build a failed indexing record without a valid embedding bundle."""

    source_pdf_id = embedding_artifact_path.name.removesuffix(".embeddings.json")
    return EmbeddingIndexingRecord(
        source_pdf_id=source_pdf_id,
        embedding_artifact_path=str(embedding_artifact_path),
        qdrant_collection=settings.qdrant_collection,
        indexed_point_count=0,
        indexing_status="failed",
        error_message=error_message,
        indexed_at=datetime.now(UTC),
    )


def is_transient_qdrant_error(exc: Exception) -> bool:
    """Return whether an indexing exception is retryable."""

    return bool(
        getattr(exc, "transient", False)
        or isinstance(exc, TimeoutError)
        or isinstance(exc, ConnectionError)
    )


def sleep_with_backoff(delay_seconds: float) -> None:
    """Sleep for the configured retry backoff duration."""

    time.sleep(delay_seconds)


def upsert_points_with_retry(
    *,
    client: object,
    settings: Settings,
    points: list[object],
    max_retries: int,
    retry_backoff_seconds: float,
) -> None:
    """Upsert Qdrant points with deterministic retry behavior."""

    attempt = 0
    while True:
        try:
            client.upsert(collection_name=settings.qdrant_collection, points=points, wait=True)
            return
        except Exception as exc:
            if attempt >= max_retries or not is_transient_qdrant_error(exc):
                raise
            sleep_with_backoff(retry_backoff_seconds * (2**attempt))
            attempt += 1


def smoke_validate_indexing(client: object, settings: Settings, expected_points: int) -> None:
    """Run a narrow operational smoke check after indexing."""

    count_response = client.count(collection_name=settings.qdrant_collection, exact=True)
    count_value = getattr(count_response, "count", None)
    if not isinstance(count_value, int) or count_value < min(expected_points, 1):
        raise RuntimeError("Qdrant smoke validation did not confirm indexed points.")


def index_embedding_bundle(
    *,
    embedding_artifact_path: Path,
    client: object,
    settings: Settings,
    max_retries: int,
    retry_backoff_seconds: float,
) -> EmbeddingIndexingRecord:
    """Index one embedding bundle into Qdrant."""

    embedding_bundle = load_embedding_bundle(embedding_artifact_path)
    ensure_qdrant_collection(client, settings, embedding_bundle.vector_dimension)
    points = build_qdrant_points(embedding_bundle)
    upsert_points_with_retry(
        client=client,
        settings=settings,
        points=points,
        max_retries=max_retries,
        retry_backoff_seconds=retry_backoff_seconds,
    )
    smoke_validate_indexing(client, settings, len(points))
    return build_indexing_record(
        embedding_bundle=embedding_bundle,
        settings=settings,
        indexing_status="succeeded",
        indexed_point_count=len(points),
    )


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
    input_dir: Path,
    source_pdf_path: Path,
    markdown_dir: Path,
    processed_dir: Path,
    overwrite: bool,
    chunk_size: int,
    chunk_overlap: int,
    pdf_conversion_backend: str,
    docling_startup_timeout_seconds: float,
    metadata_overlays: dict[str, DocumentMetadataOverlayEntry] | None = None,
) -> ProcessedDocument:
    """Ingest one source PDF according to the deterministic storage rules."""

    source_pdf_relative_path = source_pdf_path.relative_to(input_dir)
    source_pdf_id = derive_source_pdf_id(input_dir=input_dir, source_pdf_path=source_pdf_path)
    overlay_entry = (metadata_overlays or {}).get(source_pdf_id)
    (
        markdown_output_path,
        cleaned_markdown_output_path,
        processed_output_path,
        chunk_artifact_path,
    ) = build_ingestion_artifact_paths(
        source_pdf_id=source_pdf_id,
        markdown_dir=markdown_dir,
        processed_dir=processed_dir,
    )

    if (
        not overwrite
        and markdown_output_path.exists()
        and cleaned_markdown_output_path.exists()
        and processed_output_path.exists()
        and chunk_artifact_path.exists()
    ):
        return build_processed_document(
            source_pdf_id=source_pdf_id,
            source_pdf_path=source_pdf_path,
            source_pdf_relative_path=source_pdf_relative_path,
            markdown_output_path=markdown_output_path,
            cleaned_markdown_output_path=cleaned_markdown_output_path,
            processed_output_path=processed_output_path,
            ingestion_status="skipped",
            document_type=overlay_entry.document_type if overlay_entry else None,
            product=overlay_entry.product if overlay_entry else None,
        )

    raw_markdown_text = convert_pdf_to_markdown_with_backend(
        source_pdf_path,
        backend=pdf_conversion_backend,
        docling_startup_timeout_seconds=docling_startup_timeout_seconds,
    )
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
        source_pdf_id=source_pdf_id,
        source_pdf_path=source_pdf_path,
        source_pdf_relative_path=source_pdf_relative_path,
        markdown_output_path=markdown_output_path,
        cleaned_markdown_output_path=cleaned_markdown_output_path,
        processed_output_path=processed_output_path,
        ingestion_status="succeeded",
        document_name=document_name,
        document_version=document_version,
        document_type=overlay_entry.document_type if overlay_entry else None,
        product=overlay_entry.product if overlay_entry else None,
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
    metadata_overlay_path = Path(args.metadata_overlay_path) if args.metadata_overlay_path else None

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Input directory does not exist: {input_dir}", file=sys.stderr)
        return 2

    ensure_pdf_conversion_backend_available(backend=args.pdf_conversion_backend)
    metadata_overlays = load_document_metadata_overlays(metadata_overlay_path)

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
                input_dir=input_dir,
                source_pdf_path=source_pdf_path,
                markdown_dir=markdown_dir,
                processed_dir=processed_dir,
                overwrite=args.overwrite,
                chunk_size=args.chunk_size,
                chunk_overlap=args.chunk_overlap,
                pdf_conversion_backend=args.pdf_conversion_backend,
                docling_startup_timeout_seconds=args.docling_startup_timeout_seconds,
                metadata_overlays=metadata_overlays,
            )
        except Exception as exc:
            encountered_failures = True
            source_pdf_relative_path = source_pdf_path.relative_to(input_dir)
            source_pdf_id = derive_source_pdf_id(
                input_dir=input_dir,
                source_pdf_path=source_pdf_path,
            )
            (
                markdown_output_path,
                cleaned_markdown_output_path,
                processed_output_path,
                chunk_artifact_path,
            ) = build_ingestion_artifact_paths(
                source_pdf_id=source_pdf_id,
                markdown_dir=markdown_dir,
                processed_dir=processed_dir,
            )
            overlay_entry = metadata_overlays.get(source_pdf_id)
            remove_artifact_if_exists(cleaned_markdown_output_path)
            remove_artifact_if_exists(processed_output_path)
            remove_artifact_if_exists(chunk_artifact_path)
            record = build_processed_document(
                source_pdf_id=source_pdf_id,
                source_pdf_path=source_pdf_path,
                source_pdf_relative_path=source_pdf_relative_path,
                markdown_output_path=markdown_output_path,
                cleaned_markdown_output_path=cleaned_markdown_output_path,
                processed_output_path=processed_output_path,
                ingestion_status="failed",
                document_type=overlay_entry.document_type if overlay_entry else None,
                product=overlay_entry.product if overlay_entry else None,
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


def run_docling_warmup(args: argparse.Namespace) -> int:
    """Warm up Docling locally by allowing model/assets download on one sample PDF."""

    sample_pdf = Path(args.sample_pdf)
    if not sample_pdf.exists() or not sample_pdf.is_file():
        print(f"Sample PDF does not exist: {sample_pdf}", file=sys.stderr)
        return 2

    ensure_pdf_conversion_backend_available(backend="docling")
    markdown = convert_pdf_to_markdown_with_docling(
        sample_pdf,
        startup_timeout_seconds=args.docling_startup_timeout_seconds,
    )
    if not markdown.strip():
        print("Docling warm-up did not produce markdown output.", file=sys.stderr)
        return 1
    print(
        f"Docling warm-up succeeded for {sample_pdf.name}. "
        "Required assets should now be cached locally."
    )
    return 0


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


def run_qdrant_indexing(args: argparse.Namespace) -> int:
    """Execute the offline Qdrant indexing flow."""

    embedding_dir = Path(args.embedding_dir)
    manifest_path = Path(args.manifest_path)

    if not embedding_dir.exists() or not embedding_dir.is_dir():
        print(f"Embedding directory does not exist: {embedding_dir}", file=sys.stderr)
        return 2

    settings = validate_startup_settings(get_settings(), require_qdrant=True)
    ensure_qdrant_backend_available()

    embedding_artifacts = iter_embedding_artifacts(embedding_dir, args.glob)
    if not embedding_artifacts:
        print(
            f"No embedding artifacts matched glob '{args.glob}' in embedding directory: "
            f"{embedding_dir}",
            file=sys.stderr,
        )
        return 2

    client = create_qdrant_client(settings)
    encountered_failures = False

    for embedding_artifact_path in embedding_artifacts:
        try:
            record = index_embedding_bundle(
                embedding_artifact_path=embedding_artifact_path,
                client=client,
                settings=settings,
                max_retries=args.max_retries,
                retry_backoff_seconds=args.retry_backoff_seconds,
            )
        except Exception as exc:
            encountered_failures = True
            try:
                embedding_bundle = load_embedding_bundle(embedding_artifact_path)
                record = build_indexing_record(
                    embedding_bundle=embedding_bundle,
                    settings=settings,
                    indexing_status="failed",
                    indexed_point_count=0,
                    error_message=str(exc),
                )
            except Exception as load_exc:
                record = build_failed_indexing_record_from_artifact_path(
                    embedding_artifact_path=embedding_artifact_path,
                    settings=settings,
                    error_message=f"{exc}; embedding artifact load failed: {load_exc}",
                )

        append_indexing_manifest_record(manifest_path, record)

        if record.indexing_status == "failed":
            print(
                f"Failed to index embeddings for {embedding_artifact_path.name}: "
                f"{record.error_message}",
                file=sys.stderr,
            )
            if args.fail_fast:
                return 1

    return 0 if not (encountered_failures and args.fail_fast) else 1


def run_retrieval(args: argparse.Namespace, *, request_id: str | None = None) -> int:
    """Execute the first retrieval pipeline over indexed Qdrant data."""

    retrieval_query = RetrievalQuery(
        query=args.query,
        top_k=args.top_k if args.top_k is not None else get_settings().top_k,
        filters={
            "document_type": args.document_type,
            "product": args.product,
            "document_name": args.document_name,
            "version": args.version,
        },
    )
    result = retrieve_ranked_chunks(retrieval_query, request_id=request_id)
    print(result.model_dump_json(indent=2))
    return 0


def run_grounded_answer_generation(
    args: argparse.Namespace,
    *,
    request_id: str | None = None,
) -> int:
    """Execute the first grounded answer-generation workflow."""

    retrieval_query = RetrievalQuery(
        query=args.query,
        top_k=args.top_k if args.top_k is not None else get_settings().top_k,
        filters={
            "document_type": args.document_type,
            "product": args.product,
            "document_name": args.document_name,
            "version": args.version,
        },
    )
    result = generate_grounded_answer(retrieval_query, request_id=request_id)
    print(result.model_dump_json(indent=2))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint for the current offline ingestion, embedding, and indexing pipeline."""

    settings = get_settings()
    configure_logging(settings.log_level)
    log_startup_diagnostics(RAG_LOGGER, settings, runtime_surface="cli")

    parser = build_parser()
    args = parser.parse_args(argv)
    request_id = generate_request_id("cli")
    log_event(
        RAG_LOGGER,
        event_type="request_started",
        request_id=request_id,
        runtime_surface="cli",
        command=args.command,
    )

    try:
        if args.command == "ingest-pdfs":
            exit_code = run_ingestion(args)
        elif args.command == "warmup-docling-assets":
            exit_code = run_docling_warmup(args)
        elif args.command == "generate-embeddings":
            exit_code = run_embedding_generation(args)
        elif args.command == "index-embeddings":
            exit_code = run_qdrant_indexing(args)
        elif args.command == "retrieve-chunks":
            exit_code = run_retrieval(args, request_id=request_id)
        elif args.command == "answer-query":
            exit_code = run_grounded_answer_generation(args, request_id=request_id)
        else:
            parser.error(f"Unsupported command: {args.command}")
        if exit_code == 0:
            log_event(
                RAG_LOGGER,
                event_type="request_succeeded",
                request_id=request_id,
                runtime_surface="cli",
                command=args.command,
                exit_code=exit_code,
            )
        else:
            log_event(
                RAG_LOGGER,
                event_type="request_failed",
                request_id=request_id,
                level=logging.ERROR,
                runtime_surface="cli",
                command=args.command,
                error_type="CommandExit",
                error_message=f"Command exited with status {exit_code}.",
                exit_code=exit_code,
            )
        return exit_code
    except Exception as exc:
        log_event(
            RAG_LOGGER,
            event_type="request_failed",
            request_id=request_id,
            level=logging.ERROR,
            runtime_surface="cli",
            command=args.command,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
