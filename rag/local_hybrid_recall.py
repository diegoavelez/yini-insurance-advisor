from __future__ import annotations

from collections.abc import Callable, Sequence
from functools import lru_cache
from pathlib import Path

from contracts import ChunkBundle, ChunkRecord, RetrievalQuery, RetrievedChunk, TermEquivalenceSet
from rag.document_canonicalization import infer_canonical_product_from_relative_path
from rag.evidence_selection import (
    QUERY_COVERAGE_INTENT_PHRASES,
    label_surface_has_explicit_coverage_section,
    query_has_movilidad_suscripcion_billing_by_insured_intent,
    query_has_movilidad_suscripcion_collective_billing_intent,
    query_has_movilidad_suscripcion_individual_financing_intent,
)
from rag.markdown_chunk_normalization import is_pv_applicability_section_path
from rag.term_equivalences import (
    augment_query_with_term_equivalences,
    normalize_equivalence_text,
    query_contains_equivalent_phrase,
    tokenize_lexical_surface,
)

DEFAULT_CHUNK_DIR = "data/processed/chunks"


def build_hybrid_recall_terms(
    query: str,
    *,
    matched_expansion_rules: Sequence[object],
) -> list[str]:
    """Build deterministic lexical-recall phrases for one retrieval query."""

    ordered_terms: list[str] = []
    seen_terms: set[str] = set()
    anchor_token_sets = [
        tokenize_lexical_surface(" ".join(matched_rule.all_of))
        for matched_rule in matched_expansion_rules
        if matched_rule.all_of
    ]

    def append_term_if_new(term: str, *, allow_anchor_overlap: bool = False) -> None:
        normalized_term = normalize_equivalence_text(term)
        if not normalized_term or normalized_term in seen_terms:
            return
        term_tokens = tokenize_lexical_surface(term)
        if (
            not allow_anchor_overlap
            and any(
                anchor_tokens and anchor_tokens.issubset(term_tokens)
                for anchor_tokens in anchor_token_sets
            )
        ):
            return
        seen_terms.add(normalized_term)
        ordered_terms.append(term)

    append_term_if_new(query, allow_anchor_overlap=True)
    for matched_rule in matched_expansion_rules:
        for term in matched_rule.append_terms:
            append_term_if_new(term)
    return ordered_terms


def build_collective_billing_hybrid_recall_terms(query: str) -> list[str]:
    """Return narrow lexical recall terms for suscripción collective billing queries."""

    if not query_has_movilidad_suscripcion_collective_billing_intent(query):
        return []

    ordered_terms: list[str] = []
    seen_terms: set[str] = set()
    for term in (
        query,
        "pólizas colectivas",
        "modalidades de facturación",
        "facturación agrupada con devolución por asegurado",
        "devolución por asegurado",
    ):
        normalized_term = normalize_equivalence_text(term)
        if not normalized_term or normalized_term in seen_terms:
            continue
        seen_terms.add(normalized_term)
        ordered_terms.append(term)
    return ordered_terms


def build_billing_by_insured_hybrid_recall_terms(query: str) -> list[str]:
    """Return narrow lexical recall terms for suscripción billing-by-insured queries."""

    if not query_has_movilidad_suscripcion_billing_by_insured_intent(query):
        return []

    ordered_terms: list[str] = []
    seen_terms: set[str] = set()
    for term in (
        query,
        "pólizas colectivas",
        "facturación por asegurado",
        "cada asegurado",
        "modalidad de facturación",
    ):
        normalized_term = normalize_equivalence_text(term)
        if not normalized_term or normalized_term in seen_terms:
            continue
        seen_terms.add(normalized_term)
        ordered_terms.append(term)
    return ordered_terms


def build_individual_financing_hybrid_recall_terms(query: str) -> list[str]:
    """Return narrow lexical recall terms for suscripción individual financing queries."""

    if not query_has_movilidad_suscripcion_individual_financing_intent(query):
        return []

    ordered_terms: list[str] = []
    seen_terms: set[str] = set()
    for term in (
        query,
        "pólizas individuales",
        "financiación de pólizas individuales",
        "anual financiada",
        "beneficiario oneroso",
    ):
        normalized_term = normalize_equivalence_text(term)
        if not normalized_term or normalized_term in seen_terms:
            continue
        seen_terms.add(normalized_term)
        ordered_terms.append(term)
    return ordered_terms


@lru_cache(maxsize=1)
def load_local_chunk_corpus(chunk_dir: str = DEFAULT_CHUNK_DIR) -> tuple[ChunkRecord, ...]:
    """Load the local chunk corpus for optional hybrid lexical recall."""

    resolved_chunk_dir = Path(chunk_dir)
    if not resolved_chunk_dir.exists():
        return ()

    chunk_records: list[ChunkRecord] = []
    for chunk_artifact_path in sorted(resolved_chunk_dir.glob("*.chunks.json")):
        if not chunk_artifact_path.is_file():
            continue
        chunk_records.extend(
            ChunkBundle.model_validate_json(
                chunk_artifact_path.read_text(encoding="utf-8")
            ).chunks
        )
    return tuple(chunk_records)


def chunk_record_matches_filters(
    chunk_record: ChunkRecord,
    filters: object,
    *,
    term_equivalences: TermEquivalenceSet,
) -> bool:
    """Return whether one local chunk record satisfies retrieval filters."""

    resolved_product = chunk_record.product or infer_canonical_product_from_relative_path(
        chunk_record.source_pdf_relative_path,
        term_equivalences=term_equivalences,
    )
    filter_mappings = (
        ("document_type", chunk_record.document_type),
        ("product", resolved_product),
        ("document_name", chunk_record.document_name),
        ("version", chunk_record.document_version),
    )
    for filter_name, chunk_value in filter_mappings:
        filter_value = getattr(filters, filter_name, None)
        if filter_value is None:
            continue
        if chunk_value != filter_value:
            return False
    return True


def score_chunk_record_for_hybrid_recall(
    chunk_record: ChunkRecord,
    *,
    query: str,
    lexical_terms: Sequence[str],
) -> float:
    """Score one local chunk record for deterministic lexical comparison recall."""

    if not lexical_terms:
        return 0.0

    label_surface = "\n".join(
        value
        for value in (
            chunk_record.document_name,
            chunk_record.section,
            *chunk_record.section_path,
        )
        if value
    )
    body_surface = chunk_record.text
    label_tokens = tokenize_lexical_surface(label_surface)
    body_tokens = tokenize_lexical_surface(body_surface)
    deductible_intent = query_contains_equivalent_phrase(query, "deducible")
    coverage_intent = any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in QUERY_COVERAGE_INTENT_PHRASES
    )

    total_score = 0.0
    if deductible_intent and query_contains_equivalent_phrase(label_surface, "deducible"):
        total_score += 2.0
    if coverage_intent and label_surface_has_explicit_coverage_section(label_surface):
        total_score += 1.75
    for term in lexical_terms:
        normalized_term = normalize_equivalence_text(term)
        if not normalized_term:
            continue
        term_tokens = tokenize_lexical_surface(term)
        if query_contains_equivalent_phrase(label_surface, term):
            total_score += 2.0
            continue
        if query_contains_equivalent_phrase(body_surface, term):
            total_score += 1.0
            continue
        if term_tokens and term_tokens.issubset(label_tokens):
            total_score += 1.25
            continue
        if term_tokens and term_tokens.issubset(body_tokens):
            total_score += 0.75
            continue
        if term_tokens:
            label_overlap = len(term_tokens & label_tokens) / len(term_tokens)
            body_overlap = len(term_tokens & body_tokens) / len(term_tokens)
            total_score += max(label_overlap * 0.5, body_overlap * 0.25)
    return total_score


def build_retrieved_chunk_from_chunk_record(
    chunk_record: ChunkRecord,
    *,
    score: float,
) -> RetrievedChunk:
    """Map one local chunk record into a retrieval result item."""

    return RetrievedChunk(
        chunk_id=chunk_record.chunk_id,
        source_pdf_id=chunk_record.source_pdf_id,
        source_pdf_relative_path=chunk_record.source_pdf_relative_path,
        chunk_schema_version=chunk_record.chunk_schema_version,
        chunk_index=chunk_record.chunk_index,
        text=chunk_record.text,
        document_name=chunk_record.document_name,
        document_version=chunk_record.document_version,
        document_type=chunk_record.document_type,
        product=chunk_record.product,
        page=None,
        section=chunk_record.section,
        section_path=list(chunk_record.section_path),
        clause_id=None,
        score=score,
    )


def retrieve_local_lexical_candidates(
    retrieval_query: RetrievalQuery,
    *,
    term_equivalences: TermEquivalenceSet,
    matched_expansion_rules: Sequence[object],
    candidate_limit: int,
    load_local_chunk_corpus_fn: Callable[[], Sequence[ChunkRecord]] = load_local_chunk_corpus,
) -> list[RetrievedChunk]:
    """Return deterministic local lexical candidates for comparison-oriented queries."""

    if candidate_limit < 1:
        return []

    lexical_terms = build_hybrid_recall_terms(
        retrieval_query.query,
        matched_expansion_rules=matched_expansion_rules,
    )
    if not lexical_terms:
        lexical_terms = build_individual_financing_hybrid_recall_terms(
            retrieval_query.query
        )
    if not lexical_terms:
        lexical_terms = build_billing_by_insured_hybrid_recall_terms(
            retrieval_query.query
        )
    if not lexical_terms:
        lexical_terms = build_collective_billing_hybrid_recall_terms(
            retrieval_query.query
        )
    if not lexical_terms:
        return []

    scored_candidates: list[tuple[float, int, RetrievedChunk]] = []
    for index, chunk_record in enumerate(load_local_chunk_corpus_fn()):
        if not chunk_record_matches_filters(
            chunk_record,
            retrieval_query.filters,
            term_equivalences=term_equivalences,
        ):
            continue
        lexical_score = score_chunk_record_for_hybrid_recall(
            chunk_record,
            query=retrieval_query.query,
            lexical_terms=lexical_terms,
        )
        if lexical_score <= 0:
            continue
        scored_candidates.append(
            (
                lexical_score,
                -index,
                build_retrieved_chunk_from_chunk_record(
                    chunk_record,
                    score=lexical_score,
                ),
            )
        )

    scored_candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [candidate[2] for candidate in scored_candidates[:candidate_limit]]


def merge_hybrid_retrieval_candidates(
    semantic_chunks: Sequence[RetrievedChunk],
    lexical_chunks: Sequence[RetrievedChunk],
) -> list[RetrievedChunk]:
    """Merge semantic and lexical candidates with deterministic score fusion."""

    merged_candidates: dict[str, RetrievedChunk] = {
        chunk.chunk_id: chunk for chunk in semantic_chunks
    }
    for lexical_chunk in lexical_chunks:
        existing_chunk = merged_candidates.get(lexical_chunk.chunk_id)
        if existing_chunk is None:
            merged_candidates[lexical_chunk.chunk_id] = lexical_chunk
            continue
        merged_candidates[lexical_chunk.chunk_id] = existing_chunk.model_copy(
            update={"score": existing_chunk.score + (lexical_chunk.score * 0.2)}
        )
    return list(merged_candidates.values())


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

    normalized_filters = {
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
    }
    skip_document_name_injection_for_individual_financing = (
        query_has_movilidad_suscripcion_individual_financing_intent(
            retrieval_query.query
        )
    )
    for query_filter_rule in term_equivalences.query_filter_rules:
        matches_all = all(
            query_contains_equivalent_phrase(retrieval_query.query, phrase)
            for phrase in query_filter_rule.all_of
        )
        matches_any = not query_filter_rule.any_of or any(
            query_contains_equivalent_phrase(retrieval_query.query, phrase)
            for phrase in query_filter_rule.any_of
        )
        if not (matches_all and matches_any):
            continue
        for field_name, field_value in query_filter_rule.filters.items():
            if field_name not in normalized_filters or normalized_filters[field_name] is not None:
                continue
            if (
                skip_document_name_injection_for_individual_financing
                and field_name == "document_name"
            ):
                continue
            if field_name in {"document_type", "product"}:
                normalized_filters[field_name] = canonicalize_filter_value(
                    field_name=field_name,
                    value=field_value,
                    term_equivalences=term_equivalences,
                )
                continue
            normalized_filters[field_name] = field_value

    return RetrievalQuery(
        query=augment_query_with_term_equivalences(
            retrieval_query.query,
            term_equivalences,
        ),
        top_k=retrieval_query.top_k,
        filters=normalized_filters,
    )


def is_standalone_pv_applicability_chunk(chunk_record: ChunkRecord) -> bool:
    """Return whether one chunk is a standalone PV applicability chunk."""

    if not is_pv_applicability_section_path(chunk_record.section_path):
        return False
    return chunk_record.section == "PLANES QUE APLICA"


def deduplicate_exact_pv_applicability_chunks(
    chunk_records: Sequence[ChunkRecord],
    *,
    chunk_schema_version: str = "v2",
) -> list[ChunkRecord]:
    """Drop exact duplicate standalone PV applicability chunks conservatively."""

    deduplicated_records: list[ChunkRecord] = []
    seen_surfaces: set[tuple[str, str]] = set()

    for chunk_record in chunk_records:
        if not is_standalone_pv_applicability_chunk(chunk_record):
            deduplicated_records.append(chunk_record)
            continue
        normalized_text = normalize_equivalence_text(chunk_record.text)
        dedup_key = (chunk_record.source_pdf_id, normalized_text)
        if dedup_key in seen_surfaces:
            continue
        seen_surfaces.add(dedup_key)
        deduplicated_records.append(chunk_record)

    rebuilt_records: list[ChunkRecord] = []
    for chunk_index, chunk_record in enumerate(deduplicated_records):
        rebuilt_records.append(
            ChunkRecord(
                chunk_id=(
                    f"{chunk_record.source_pdf_id}:{chunk_schema_version}:{chunk_index:04d}"
                ),
                source_pdf_id=chunk_record.source_pdf_id,
                document_name=chunk_record.document_name,
                document_version=chunk_record.document_version,
                document_type=chunk_record.document_type,
                product=chunk_record.product,
                source_pdf_path=chunk_record.source_pdf_path,
                source_pdf_relative_path=chunk_record.source_pdf_relative_path,
                cleaned_markdown_output_path=chunk_record.cleaned_markdown_output_path,
                text=chunk_record.text,
                chunk_index=chunk_index,
                chunk_schema_version=chunk_record.chunk_schema_version,
                section=chunk_record.section,
                section_path=chunk_record.section_path,
            )
        )

    return rebuilt_records
