"""Offline PDF ingestion CLI for the current Phase 2 and early Phase 3 slices."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import logging
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path

from contracts import (
    AdvisorDraftResponse,
    ChunkBundle,
    ChunkRecord,
    DocumentMetadataOverlayEntry,
    DocumentMetadataOverlaySet,
    DocumentRetrievalResult,
    EmbeddingBundle,
    EmbeddingGenerationRecord,
    EmbeddingIndexingRecord,
    EmbeddingRecord,
    GroundedAnswerResult,
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
from rag import evidence_selection, local_hybrid_recall, pdf_conversion, qdrant_store
from rag.document_canonicalization import (
    build_ingestion_artifact_paths,
    build_processed_document,
    derive_source_pdf_id,
    extract_document_metadata,
    resolve_document_product,
    resolve_document_type,
)
from rag.grounded_answers import (
    assess_grounding as _assess_grounding,
)
from rag.grounded_answers import (
    build_citations_from_chunks as _build_citations_from_chunks,
)
from rag.grounded_answers import (
    build_documentary_basis as _build_documentary_basis,
)
from rag.grounded_answers import (
    build_grounded_prompt as _build_grounded_prompt,
)
from rag.grounded_answers import (
    build_insufficient_evidence_response as _build_insufficient_evidence_response,
)
from rag.grounded_answers import (
    build_missing_citation_guardrail_response as _build_missing_citation_guardrail_response,
)
from rag.grounded_answers import (
    build_prompt_injection_refusal_response as _build_prompt_injection_refusal_response,
)
from rag.grounded_answers import (
    build_unsupported_query_response as _build_unsupported_query_response,
)
from rag.markdown_chunk_normalization import (
    MarkdownBlock,
    ensure_chunk_text_includes_section_context,
    expand_large_blocks,
    group_semantic_blocks,
    markdown_has_non_heading_content,
    normalize_known_document_markdown,
    should_disable_chunk_overlap_for_entries,
    split_markdown_blocks,
)
from rag.markdown_chunk_normalization import (
    normalize_pv_commercial_block as _normalize_pv_commercial_block,
)
from rag.term_equivalences import (
    get_matching_query_expansion_rules,
    load_term_equivalences,
)

EMPTY_BOILERPLATE_LINES = pdf_conversion.EMPTY_BOILERPLATE_LINES
CHUNK_SCHEMA_VERSION = "v2"
DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 200
EMBEDDING_SCHEMA_VERSION = "v1"
SUPPORTED_EMBEDDING_PROVIDER = "sentence-transformers"
DEFAULT_EMBEDDING_DIR = "data/processed/embeddings"
DEFAULT_CHUNK_DIR = "data/processed/chunks"
DEFAULT_QDRANT_INDEXING_MANIFEST = "data/processed/qdrant-indexing-manifest.jsonl"
DEFAULT_QDRANT_MAX_RETRIES = 3
DEFAULT_QDRANT_RETRY_BACKOFF_SECONDS = 0.25
DEFAULT_DOCLING_STARTUP_TIMEOUT_SECONDS = 1800.0
MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE = 2
ADVISOR_REVIEW_NOTICE = "This response is a draft for advisor review."
RAG_LOGGER = logging.getLogger("yini.rag")
normalize_pv_commercial_block = _normalize_pv_commercial_block
build_qdrant_point_id = qdrant_store.build_qdrant_point_id
build_qdrant_points = qdrant_store.build_qdrant_points
build_qdrant_source_pdf_filter = qdrant_store.build_qdrant_source_pdf_filter
build_candidate_pool_limit = evidence_selection.build_candidate_pool_limit
build_grounded_prompt = _build_grounded_prompt
build_citations_from_chunks = _build_citations_from_chunks
build_documentary_basis = _build_documentary_basis
create_qdrant_client = qdrant_store.create_qdrant_client
ensure_qdrant_collection = qdrant_store.ensure_qdrant_collection
get_qdrant_models = qdrant_store.get_qdrant_models
is_transient_qdrant_error = qdrant_store.is_transient_qdrant_error
label_surface_has_explicit_coverage_section = (
    evidence_selection.label_surface_has_explicit_coverage_section
)
map_search_hit_to_retrieved_chunk = qdrant_store.map_search_hit_to_retrieved_chunk
prune_existing_source_points = qdrant_store.prune_existing_source_points
QUERY_COVERAGE_INTENT_PHRASES = evidence_selection.QUERY_COVERAGE_INTENT_PHRASES
query_has_arl_account_update_guide_intent = (
    evidence_selection.query_has_arl_account_update_guide_intent
)
query_has_arl_commissions_guide_intent = evidence_selection.query_has_arl_commissions_guide_intent
query_has_arl_rui_normativity_intent = evidence_selection.query_has_arl_rui_normativity_intent
query_has_movilidad_pv_benefit_intent = evidence_selection.query_has_movilidad_pv_benefit_intent
query_has_movilidad_suscripcion_billing_by_insured_intent = (
    evidence_selection.query_has_movilidad_suscripcion_billing_by_insured_intent
)
query_has_movilidad_suscripcion_collective_billing_intent = (
    evidence_selection.query_has_movilidad_suscripcion_collective_billing_intent
)
query_has_movilidad_suscripcion_collective_billing_renewal_intent = (
    evidence_selection.query_has_movilidad_suscripcion_collective_billing_renewal_intent
)
query_has_movilidad_suscripcion_individual_financing_intent = (
    evidence_selection.query_has_movilidad_suscripcion_individual_financing_intent
)
query_has_movilidad_suscripcion_policy_intent = (
    evidence_selection.query_has_movilidad_suscripcion_policy_intent
)
search_qdrant_chunks = qdrant_store.search_qdrant_chunks
sleep_with_backoff = qdrant_store.sleep_with_backoff
smoke_validate_indexing = qdrant_store.smoke_validate_indexing
upsert_points_with_retry = qdrant_store.upsert_points_with_retry


def assess_grounding(
    *,
    retrieved_chunks: list[RetrievedChunk],
    citations: list,
):
    """Build a typed grounding assessment from evidence availability."""

    return _assess_grounding(
        retrieved_chunks=retrieved_chunks,
        citations=citations,
        min_retrieval_chunks_for_high_confidence=MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE,
    )


def build_insufficient_evidence_response(
    *,
    query: str,
    retrieved_chunks: list[RetrievedChunk],
    limitation_note: str | None = None,
) -> GroundedAnswerResult:
    """Return a typed limited grounded response for insufficient evidence."""

    return _build_insufficient_evidence_response(
        query=query,
        retrieved_chunks=retrieved_chunks,
        limitation_note=limitation_note,
        advisor_review_notice=ADVISOR_REVIEW_NOTICE,
        min_retrieval_chunks_for_high_confidence=MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE,
    )


def build_unsupported_query_response(*, query: str) -> GroundedAnswerResult:
    """Return a typed conservative refusal for out-of-scope queries."""

    return _build_unsupported_query_response(
        query=query,
        advisor_review_notice=ADVISOR_REVIEW_NOTICE,
    )


def build_prompt_injection_refusal_response(*, query: str) -> GroundedAnswerResult:
    """Return a typed conservative refusal for prompt-injection-like queries."""

    return _build_prompt_injection_refusal_response(
        query=query,
        advisor_review_notice=ADVISOR_REVIEW_NOTICE,
    )


def build_missing_citation_guardrail_response(
    *,
    query: str,
    retrieved_chunks: list[RetrievedChunk],
) -> GroundedAnswerResult:
    """Return a typed guarded outcome for citationless answerable responses."""

    return _build_missing_citation_guardrail_response(
        query=query,
        retrieved_chunks=retrieved_chunks,
        advisor_review_notice=ADVISOR_REVIEW_NOTICE,
    )


def rerank_chunks_for_query_expansion_rules(
    chunks: Sequence[RetrievedChunk],
    *,
    query: str,
    matched_expansion_rules: Sequence[object],
    top_k: int,
) -> list[RetrievedChunk]:
    """Apply deterministic domain-specific reranking for retrieved chunks."""

    return evidence_selection.rerank_chunks_for_query_expansion_rules(
        chunks,
        query=query,
        matched_expansion_rules=matched_expansion_rules,
        top_k=top_k,
    )


def select_answer_evidence_chunks(
    retrieved_chunks: Sequence[RetrievedChunk],
    *,
    query: str,
) -> list[RetrievedChunk]:
    """Return the answer-facing evidence subset for one retrieval query."""

    return evidence_selection.select_answer_evidence_chunks(
        retrieved_chunks,
        query=query,
        min_retrieval_chunks_for_high_confidence=MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE,
    )


def select_citation_evidence_chunks(
    retrieved_chunks: Sequence[RetrievedChunk],
    *,
    query: str,
) -> list[RetrievedChunk]:
    """Return the citation-facing evidence subset for one answer query."""

    return evidence_selection.select_citation_evidence_chunks(
        retrieved_chunks,
        query=query,
    )


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

    subparsers.add_parser("warmup-embedding-assets")

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


docling_is_available = pdf_conversion.docling_is_available
ensure_docling_available = pdf_conversion.ensure_docling_available
pdfium_backend_is_available = pdf_conversion.pdfium_backend_is_available


def ensure_pdf_conversion_backend_available(
    *,
    backend: str,
    docling_is_available_fn=None,
    pdfium_backend_is_available_fn=None,
) -> None:
    """Fail loudly when no supported local PDF conversion backend is available."""

    return pdf_conversion.ensure_pdf_conversion_backend_available(
        backend=backend,
        docling_is_available_fn=docling_is_available_fn or docling_is_available,
        pdfium_backend_is_available_fn=(
            pdfium_backend_is_available_fn or pdfium_backend_is_available
        ),
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


@lru_cache(maxsize=8)
def load_sentence_transformer(model_name: str, *, local_files_only: bool = True):
    """Return a cached SentenceTransformer instance for deterministic reuse."""

    try:
        with offline_huggingface_resolution(enabled=local_files_only):
            sentence_transformers = importlib.import_module("sentence_transformers")
            return sentence_transformers.SentenceTransformer(
                model_name,
                local_files_only=local_files_only,
            )
    except TypeError:
        if local_files_only:
            raise RuntimeError(
                "Installed sentence-transformers version does not support offline "
                "local_files_only loading."
            ) from None
        return sentence_transformers.SentenceTransformer(model_name)


offline_huggingface_resolution = pdf_conversion.offline_huggingface_resolution


def ensure_embedding_model_assets_available(settings: Settings) -> None:
    """Fail loudly when embedding-model assets are not cached locally."""

    try:
        load_sentence_transformer(settings.embedding_model, local_files_only=True)
    except Exception as exc:
        raise RuntimeError(
            "Embedding model assets are not cached locally for "
            f"{settings.embedding_model}. Run `python -m rag.ingestion "
            "warmup-embedding-assets` once with network access, or pre-populate "
            "the Hugging Face cache before running offline embedding or retrieval commands."
        ) from exc


def generate_embedding_vector(text: str, settings: Settings) -> list[float]:
    """Generate one embedding vector for chunk text."""

    if settings.embedding_provider != SUPPORTED_EMBEDDING_PROVIDER:
        raise RuntimeError("Unsupported embedding provider for local embedding generation.")

    ensure_embedding_model_assets_available(settings)
    model = load_sentence_transformer(settings.embedding_model, local_files_only=True)
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


convert_pdf_to_markdown_with_docling = pdf_conversion.convert_pdf_to_markdown_with_docling
convert_pdf_to_markdown_with_pdfium = pdf_conversion.convert_pdf_to_markdown_with_pdfium
markdown_has_usable_text_surface = pdf_conversion.markdown_has_usable_text_surface
is_docling_insufficient_text_error = pdf_conversion.is_docling_insufficient_text_error


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

    return pdf_conversion.convert_pdf_to_markdown_with_backend(
        source_pdf_path,
        backend=backend,
        docling_startup_timeout_seconds=docling_startup_timeout_seconds,
        docling_is_available_fn=docling_is_available,
        pdfium_backend_is_available_fn=pdfium_backend_is_available,
        convert_pdf_to_markdown_with_docling_fn=convert_pdf_to_markdown_with_docling,
        convert_pdf_to_markdown_with_pdfium_fn=convert_pdf_to_markdown_with_pdfium,
        markdown_has_usable_text_surface_fn=markdown_has_usable_text_surface,
        is_docling_insufficient_text_error_fn=is_docling_insufficient_text_error,
        ensure_pdf_conversion_backend_available_fn=ensure_pdf_conversion_backend_available,
    )


clean_markdown = pdf_conversion.clean_markdown


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


build_hybrid_recall_terms = local_hybrid_recall.build_hybrid_recall_terms
build_collective_billing_hybrid_recall_terms = (
    local_hybrid_recall.build_collective_billing_hybrid_recall_terms
)
build_billing_by_insured_hybrid_recall_terms = (
    local_hybrid_recall.build_billing_by_insured_hybrid_recall_terms
)
build_individual_financing_hybrid_recall_terms = (
    local_hybrid_recall.build_individual_financing_hybrid_recall_terms
)
chunk_record_matches_filters = local_hybrid_recall.chunk_record_matches_filters
score_chunk_record_for_hybrid_recall = local_hybrid_recall.score_chunk_record_for_hybrid_recall
build_retrieved_chunk_from_chunk_record = (
    local_hybrid_recall.build_retrieved_chunk_from_chunk_record
)
merge_hybrid_retrieval_candidates = (
    local_hybrid_recall.merge_hybrid_retrieval_candidates
)
canonicalize_filter_value = local_hybrid_recall.canonicalize_filter_value
normalize_retrieval_query_with_term_equivalences = (
    local_hybrid_recall.normalize_retrieval_query_with_term_equivalences
)
load_local_chunk_corpus = local_hybrid_recall.load_local_chunk_corpus


def retrieve_local_lexical_candidates(
    retrieval_query: RetrievalQuery,
    *,
    term_equivalences: TermEquivalenceSet,
    matched_expansion_rules: Sequence[object],
    candidate_limit: int,
) -> list[RetrievedChunk]:
    """Return deterministic local lexical candidates for comparison-oriented queries."""

    return local_hybrid_recall.retrieve_local_lexical_candidates(
        retrieval_query,
        term_equivalences=term_equivalences,
        matched_expansion_rules=matched_expansion_rules,
        candidate_limit=candidate_limit,
        load_local_chunk_corpus_fn=load_local_chunk_corpus,
    )


def deduplicate_exact_pv_applicability_chunks(
    chunk_records: Sequence[ChunkRecord],
) -> list[ChunkRecord]:
    """Drop exact duplicate standalone PV applicability chunks conservatively."""

    return local_hybrid_recall.deduplicate_exact_pv_applicability_chunks(
        chunk_records,
        chunk_schema_version=CHUNK_SCHEMA_VERSION,
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


def remove_artifact_if_exists(path: Path) -> None:
    """Delete an artifact path when it already exists."""

    if path.exists():
        path.unlink()


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
            if current_entries and block.section_path != current_entries[-1].section_path:
                break
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
        chunk_text = ensure_chunk_text_includes_section_context(
            chunk_text=chunk_text,
            section_path=chunk_section_path,
        )
        if not markdown_has_non_heading_content(chunk_text):
            if end_index >= len(blocks):
                break
        else:
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

        if should_disable_chunk_overlap_for_entries(current_entries):
            start_index = end_index
            continue

        overlap_block_count = 0
        overlap_length = 0
        cursor = len(current_entries) - 1
        while cursor >= 0 and overlap_length < chunk_overlap:
            overlap_length += len(current_entries[cursor].text)
            overlap_block_count += 1
            cursor -= 1

        next_start_index = end_index - overlap_block_count
        start_index = max(next_start_index, start_index + 1)

    return deduplicate_exact_pv_applicability_chunks(chunk_records)


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


def existing_ingestion_artifacts_match_resolved_metadata(
    *,
    processed_output_path: Path,
    chunk_artifact_path: Path,
    resolved_document_type: str | None,
    resolved_product: str | None,
) -> bool:
    """Return whether persisted ingestion artifacts still match current metadata."""

    try:
        processed_document = ProcessedDocument.model_validate_json(
            processed_output_path.read_text(encoding="utf-8")
        )
        chunk_bundle = load_chunk_bundle(chunk_artifact_path)
    except Exception:
        return False

    return (
        processed_document.document_type == resolved_document_type
        and processed_document.product == resolved_product
        and chunk_bundle.document_type == resolved_document_type
        and chunk_bundle.product == resolved_product
    )


def existing_embedding_artifact_matches_chunk_bundle(
    *,
    embedding_artifact_path: Path,
    chunk_bundle: ChunkBundle,
) -> bool:
    """Return whether one persisted embedding artifact still matches its chunk bundle."""

    try:
        embedding_bundle = load_embedding_bundle(embedding_artifact_path)
    except Exception:
        return False

    if (
        embedding_bundle.document_name != chunk_bundle.document_name
        or embedding_bundle.document_version != chunk_bundle.document_version
        or embedding_bundle.document_type != chunk_bundle.document_type
        or embedding_bundle.product != chunk_bundle.product
        or embedding_bundle.chunk_schema_version != chunk_bundle.chunk_schema_version
    ):
        return False

    expected_chunk_ids = [chunk.chunk_id for chunk in chunk_bundle.chunks]
    actual_chunk_ids = [record.chunk_id for record in embedding_bundle.embeddings]
    if actual_chunk_ids != expected_chunk_ids:
        return False

    actual_payload_metadata = [
        (
            record.payload.document_name,
            record.payload.document_version,
            record.payload.document_type,
            record.payload.product,
        )
        for record in embedding_bundle.embeddings
    ]
    expected_payload_metadata = [
        (
            chunk.document_name,
            chunk.document_version,
            chunk.document_type,
            chunk.product,
        )
        for chunk in chunk_bundle.chunks
    ]
    return actual_payload_metadata == expected_payload_metadata


def iter_embedding_artifacts(embedding_dir: Path, glob_pattern: str) -> list[Path]:
    """Return sorted matching embedding artifacts under the configured directory."""

    return sorted(path for path in embedding_dir.glob(glob_pattern) if path.is_file())


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
        term_equivalences = load_term_equivalences()
        normalized_retrieval_query = normalize_retrieval_query_with_term_equivalences(
            retrieval_query,
            term_equivalences=term_equivalences,
        )
        matched_expansion_rules = get_matching_query_expansion_rules(
            retrieval_query.query,
            term_equivalences=term_equivalences,
        )
        ensure_qdrant_backend_available()
        resolved_client = client or create_qdrant_client(resolved_settings)
        query_vector = generate_embedding_vector(
            normalized_retrieval_query.query,
            resolved_settings,
        )
        candidate_pool_limit = build_candidate_pool_limit(
            query=normalized_retrieval_query.query,
            top_k=normalized_retrieval_query.top_k,
            matched_expansion_rules=matched_expansion_rules,
        )
        hits = search_qdrant_chunks(
            client=resolved_client,
            settings=resolved_settings,
            retrieval_query=normalized_retrieval_query,
            query_vector=query_vector,
            candidate_limit=candidate_pool_limit,
        )
        retrieved_chunks = [map_search_hit_to_retrieved_chunk(hit) for hit in hits]
        retrieved_chunks = merge_hybrid_retrieval_candidates(
            retrieved_chunks,
            retrieve_local_lexical_candidates(
                normalized_retrieval_query,
                term_equivalences=term_equivalences,
                matched_expansion_rules=matched_expansion_rules,
                candidate_limit=candidate_pool_limit,
            ),
        )
        result = DocumentRetrievalResult(
            chunks=rerank_chunks_for_query_expansion_rules(
                retrieved_chunks,
                query=retrieval_query.query,
                matched_expansion_rules=matched_expansion_rules,
                top_k=normalized_retrieval_query.top_k,
            )
        )
        return result


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
            result = _build_prompt_injection_refusal_response(
                query=retrieval_query.query,
                advisor_review_notice=ADVISOR_REVIEW_NOTICE,
            )
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
            result = _build_unsupported_query_response(
                query=retrieval_query.query,
                advisor_review_notice=ADVISOR_REVIEW_NOTICE,
            )
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
        answer_evidence_chunks = select_answer_evidence_chunks(
            retrieved_chunks,
            query=retrieval_query.query,
        )
        if not answer_evidence_chunks:
            result = _build_insufficient_evidence_response(
                query=retrieval_query.query,
                retrieved_chunks=answer_evidence_chunks,
                advisor_review_notice=ADVISOR_REVIEW_NOTICE,
                min_retrieval_chunks_for_high_confidence=(
                    MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE
                ),
            )
            return result
        if len(answer_evidence_chunks) < MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE:
            result = _build_insufficient_evidence_response(
                query=retrieval_query.query,
                retrieved_chunks=answer_evidence_chunks,
                limitation_note=(
                    "Retrieved evidence is too limited to support a strong grounded answer."
                ),
                advisor_review_notice=ADVISOR_REVIEW_NOTICE,
                min_retrieval_chunks_for_high_confidence=(
                    MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE
                ),
            )
            return result

        citation_evidence_chunks = select_citation_evidence_chunks(
            answer_evidence_chunks,
            query=retrieval_query.query,
        )
        citations = build_citations_from_chunks(citation_evidence_chunks)
        if not citations:
            log_event(
                RAG_LOGGER,
                event_type="citation_presence_guardrail_triggered",
                request_id=request_id,
                guardrail_surface="grounded_answer_generation",
                retrieved_chunk_count=len(answer_evidence_chunks),
                citation_count=0,
            )
            result = _build_missing_citation_guardrail_response(
                query=retrieval_query.query,
                retrieved_chunks=answer_evidence_chunks,
                advisor_review_notice=ADVISOR_REVIEW_NOTICE,
            )
            return result
        prompt = build_grounded_prompt(
            query=retrieval_query.query,
            retrieved_chunks=answer_evidence_chunks,
        )
        completion_fn = completion_generator or generate_grounded_completion
        suggested_answer = completion_fn(prompt, resolved_settings)
        verification = _assess_grounding(
            retrieved_chunks=answer_evidence_chunks,
            citations=citations,
            min_retrieval_chunks_for_high_confidence=MIN_RETRIEVAL_CHUNKS_FOR_HIGH_CONFIDENCE,
        )

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
                documentary_basis=build_documentary_basis(citation_evidence_chunks),
                citations=citations,
                confidence=confidence,
                limitations=limitations,
                advisor_review_notice=ADVISOR_REVIEW_NOTICE,
            ),
            verification=verification,
        )
        return result


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
    prune_existing_source_points(
        client=client,
        settings=settings,
        source_pdf_id=embedding_bundle.source_pdf_id,
    )
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

    if (
        not overwrite
        and embedding_artifact_path.exists()
        and existing_embedding_artifact_matches_chunk_bundle(
            embedding_artifact_path=embedding_artifact_path,
            chunk_bundle=chunk_bundle,
        )
    ):
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
    term_equivalences: TermEquivalenceSet | None = None,
) -> ProcessedDocument:
    """Ingest one source PDF according to the deterministic storage rules."""

    source_pdf_relative_path = source_pdf_path.relative_to(input_dir)
    source_pdf_id = derive_source_pdf_id(input_dir=input_dir, source_pdf_path=source_pdf_path)
    overlay_entry = (metadata_overlays or {}).get(source_pdf_id)
    resolved_term_equivalences = term_equivalences or load_term_equivalences()
    resolved_document_type = resolve_document_type(
        source_pdf_relative_path=source_pdf_relative_path,
        overlay_entry=overlay_entry,
        term_equivalences=resolved_term_equivalences,
    )
    resolved_product = resolve_document_product(
        source_pdf_relative_path=source_pdf_relative_path,
        overlay_entry=overlay_entry,
        term_equivalences=resolved_term_equivalences,
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

    if (
        not overwrite
        and markdown_output_path.exists()
        and cleaned_markdown_output_path.exists()
        and processed_output_path.exists()
        and chunk_artifact_path.exists()
        and existing_ingestion_artifacts_match_resolved_metadata(
            processed_output_path=processed_output_path,
            chunk_artifact_path=chunk_artifact_path,
            resolved_document_type=resolved_document_type,
            resolved_product=resolved_product,
        )
    ):
        return build_processed_document(
            source_pdf_id=source_pdf_id,
            source_pdf_path=source_pdf_path,
            source_pdf_relative_path=source_pdf_relative_path,
            markdown_output_path=markdown_output_path,
            cleaned_markdown_output_path=cleaned_markdown_output_path,
            processed_output_path=processed_output_path,
            ingestion_status="skipped",
            document_type=resolved_document_type,
            product=resolved_product,
        )

    raw_markdown_text = convert_pdf_to_markdown_with_backend(
        source_pdf_path,
        backend=pdf_conversion_backend,
        docling_startup_timeout_seconds=docling_startup_timeout_seconds,
    )
    markdown_output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_output_path.write_text(raw_markdown_text, encoding="utf-8")

    cleaned_markdown_text = normalize_known_document_markdown(
        source_pdf_path=source_pdf_path,
        cleaned_markdown_text=clean_markdown(raw_markdown_text),
    )
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
        document_type=resolved_document_type,
        product=resolved_product,
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
    term_equivalences = load_term_equivalences()

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
                term_equivalences=term_equivalences,
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
            resolved_document_type = resolve_document_type(
                source_pdf_relative_path=source_pdf_relative_path,
                overlay_entry=overlay_entry,
                term_equivalences=term_equivalences,
            )
            resolved_product = resolve_document_product(
                source_pdf_relative_path=source_pdf_relative_path,
                overlay_entry=overlay_entry,
                term_equivalences=term_equivalences,
            )
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
                document_type=resolved_document_type,
                product=resolved_product,
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


def run_embedding_warmup() -> int:
    """Warm up embedding-model assets locally by allowing one networked load."""

    settings = validate_embedding_settings(get_settings())
    ensure_embedding_backend_available(settings)
    load_sentence_transformer(settings.embedding_model, local_files_only=False)
    print(
        f"Embedding warm-up succeeded for {settings.embedding_model}. "
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
        elif args.command == "warmup-embedding-assets":
            exit_code = run_embedding_warmup()
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
