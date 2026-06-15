from __future__ import annotations

import re
from collections.abc import Sequence

from contracts import RetrievedChunk
from rag.arl_remuneration import (
    is_arl_remuneration_overview_citation_support_chunk,
    prioritize_arl_remuneration_policy_evidence,
    query_has_arl_remuneration_overview_intent,
    query_has_arl_remuneration_policy_intent,
)
from rag.term_equivalences import (
    normalize_equivalence_text,
    query_contains_equivalent_phrase,
    tokenize_lexical_surface,
)

QUERY_COVERAGE_INTENT_PHRASES = (
    "qué cubre",
    "que cubre",
    "cubre",
    "cobertura",
    "ampara",
    "amparo",
)
ARL_RUI_NORMATIVE_ANCHORS = (
    "ley 1562",
    "decreto 1117",
    "resolucion 0136",
)
EXPLICIT_COVERAGE_SECTION_PATTERN = re.compile(
    r"^(?:\d+(?:\.\d+)*\.?\s*)?cobertura(?:\s+\S.*)?$",
    re.IGNORECASE,
)
LEADING_SECTION_NUMBER_PATTERN = re.compile(r"^(\d+(?:\.\d+)*)")
DESCRIPTIVE_COVERAGE_OPENERS = (
    "si como consecuencia",
    "si le haces daño",
    "si contrataste la cobertura",
    "sura te pagará",
    "sura coordinará y pagará",
)
OPERATIONAL_COVERAGE_OPENERS = (
    "recuerda que",
    "en caso de no hacerlo",
    "cuando elijas el valor asegurado",
    "en caso de sufrir",
    "solo podrás reclamar",
    "debes realizar",
)


def label_surface_has_explicit_coverage_section(label_surface: str) -> bool:
    """Return whether one label surface contains an explicit coverage heading."""

    for raw_line in label_surface.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        normalized_line = normalize_equivalence_text(line)
        if normalized_line in {"coberturas principales", "coberturas opcionales"}:
            return True
        if EXPLICIT_COVERAGE_SECTION_PATTERN.match(line):
            return True
    return False


def build_section_sort_key(section: str | None) -> tuple[int, ...]:
    """Return a deterministic numeric-first ordering key for one section label."""

    if not section:
        return (9999,)
    match = LEADING_SECTION_NUMBER_PATTERN.match(section.strip())
    if match is None:
        return (9999,)
    return tuple(int(part) for part in match.group(1).split("."))


def coverage_section_identity(chunk: RetrievedChunk) -> tuple[str, ...]:
    """Return a stable identity for coverage-section diversification."""

    if chunk.section_path:
        return tuple(chunk.section_path)
    if chunk.section:
        return (chunk.section,)
    return (chunk.chunk_id,)


def query_has_movilidad_pv_benefit_intent(query: str) -> bool:
    """Return whether one query explicitly asks for movilidad PV benefits."""

    if not query_contains_equivalent_phrase(query, "propuesta de valor"):
        return False
    if not query_contains_equivalent_phrase(query, "movilidad"):
        return False
    return any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in (
            "beneficios",
            "beneficio",
            "incluye",
            "incluyen",
            "diferenciales",
            "ventajas",
        )
    )


def is_movilidad_pv_document_family_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one retrieved chunk belongs to the movilidad PV family."""

    return normalize_equivalence_text(chunk.document_name) == "propuesta de valor movilidad"


def query_has_movilidad_suscripcion_policy_intent(query: str) -> bool:
    """Return whether one query broadly asks for movilidad suscripción policies."""

    if not query_contains_equivalent_phrase(query, "suscripcion"):
        return False
    if not query_contains_equivalent_phrase(query, "movilidad"):
        return False
    return any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in ("politicas", "reglas", "lineamientos", "criterios")
    )


def query_has_movilidad_suscripcion_collective_billing_intent(query: str) -> bool:
    """Return whether one query explicitly asks about collective billing."""

    if not query_contains_equivalent_phrase(query, "movilidad"):
        return False
    if not query_contains_equivalent_phrase(query, "polizas colectivas"):
        return False
    return any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in ("facturacion", "cobro", "factura", "pago")
    )


def query_has_movilidad_suscripcion_billing_by_insured_intent(query: str) -> bool:
    """Return whether one query explicitly asks about billing by insured in collective policies."""

    if not any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in ("poliza colectiva", "polizas colectivas")
    ):
        return False
    if not any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in ("facturacion", "cobro", "factura")
    ):
        return False
    return any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in ("por asegurado", "asegurado", "asegurados")
    )


def query_has_movilidad_suscripcion_collective_billing_renewal_intent(query: str) -> bool:
    """Return whether one query asks about renewal-time billing-mode changes."""

    if not any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in ("poliza colectiva", "polizas colectivas")
    ):
        return False
    if not any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in ("facturacion", "forma de pago", "modalidad de facturacion")
    ):
        return False
    return any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in ("renovacion", "renovación")
    )


def query_has_movilidad_suscripcion_individual_financing_intent(query: str) -> bool:
    """Return whether one query asks about suscripción financing for individual policies."""

    if not query_contains_equivalent_phrase(query, "movilidad"):
        return False
    if not any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in ("poliza individual", "polizas individuales")
    ):
        return False
    return any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in ("financiacion", "financiada", "financiado")
    )


def is_movilidad_suscripcion_document_family_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one retrieved chunk belongs to the suscripción policy family."""

    return (
        normalize_equivalence_text(chunk.document_name)
        == "politicas de suscripcion de movilidad"
    )


def build_chunk_body_without_markdown_headings(text: str) -> str:
    """Return chunk body lines after removing markdown heading-only lines."""

    return "\n".join(
        stripped_line
        for stripped_line in (line.strip() for line in text.splitlines())
        if stripped_line and not stripped_line.startswith("#")
    )


def score_movilidad_suscripcion_evidence_richness(chunk: RetrievedChunk) -> float:
    """Return a deterministic preference score for richer suscripción evidence."""

    body_surface = build_chunk_body_without_markdown_headings(chunk.text)
    normalized_body = normalize_equivalence_text(body_surface)
    if not normalized_body:
        return -3.0

    body_lines = [line for line in body_surface.splitlines() if line.strip()]
    total_score = 0.0
    if len(normalized_body) >= 32:
        total_score += 1.0
    else:
        total_score -= 1.0
    if len(normalized_body) >= 96:
        total_score += 0.8
    if len(normalized_body) >= 180:
        total_score += 0.6
    if len(body_lines) >= 2:
        total_score += 0.35
    if count_bullet_lines(body_surface) > 0:
        total_score += 0.25
    return total_score


def is_movilidad_suscripcion_collective_billing_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk belongs to the collective billing subtree."""

    normalized_labels = [
        normalize_equivalence_text(value)
        for value in (chunk.section, *chunk.section_path)
        if value
    ]
    return any(label.startswith("14 6") or label.startswith("14.6") for label in normalized_labels)


def is_movilidad_suscripcion_collective_billing_grouped_refund_chunk(
    chunk: RetrievedChunk,
) -> bool:
    """Return whether one chunk belongs to the documented grouped-refund billing subsection."""

    normalized_labels = [
        normalize_equivalence_text(value)
        for value in (chunk.section, *chunk.section_path)
        if value
    ]
    return any(
        label.startswith("14.6.2.")
        and "facturacion" in label
        and "devolucion por asegurado" in label
        for label in normalized_labels
    )


def is_movilidad_suscripcion_individual_financing_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk belongs to the individual financing subsection."""

    normalized_labels = [
        normalize_equivalence_text(value)
        for value in (chunk.section, *chunk.section_path)
        if value
    ]
    return any(
        (
            label.startswith("13.11.")
            or label.startswith("13 11 ")
            or label == "13.11 financiacion de polizas individuales"
        )
        and "financiacion de polizas individuales" in label
        for label in normalized_labels
    )


def is_movilidad_suscripcion_individual_payment_change_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk belongs to individual payment-change rules."""

    normalized_labels = [
        normalize_equivalence_text(value)
        for value in (chunk.section, *chunk.section_path)
        if value
    ]
    return any(
        label
        in {
            "13.10. cambio en forma de pago negocio individual (produccion = cobro)",
            "13.1. 2. cambio de plan de pagos anual financiado",
        }
        for label in normalized_labels
    )


def is_movilidad_suscripcion_direct_financing_support_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk directly supports financing-individual answers."""

    return (
        is_movilidad_suscripcion_individual_financing_chunk(chunk)
        or is_movilidad_suscripcion_individual_payment_change_chunk(chunk)
    )


def is_movilidad_suscripcion_billing_by_insured_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk contains billing-by-insured evidence."""

    label_surface = "\n".join(
        value
        for value in (
            chunk.document_name,
            chunk.section,
            *chunk.section_path,
            chunk.text,
        )
        if value
    )
    return query_contains_equivalent_phrase(label_surface, "facturacion por asegurado")


def score_movilidad_suscripcion_billing_by_insured_intent_alignment(
    chunk: RetrievedChunk,
    *,
    query: str,
) -> float:
    """Return a narrow preference score for billing-by-insured prompts."""

    if not query_has_movilidad_suscripcion_billing_by_insured_intent(query):
        return 0.0
    if is_movilidad_suscripcion_billing_by_insured_chunk(chunk):
        return 3.0
    if is_movilidad_suscripcion_collective_billing_grouped_refund_chunk(chunk):
        return 0.75
    return 0.0


def score_movilidad_suscripcion_collective_billing_renewal_intent_alignment(
    chunk: RetrievedChunk,
    *,
    query: str,
) -> float:
    """Return a narrow preference score for renewal-specific collective billing prompts."""

    if not query_has_movilidad_suscripcion_collective_billing_renewal_intent(query):
        return 0.0
    if is_movilidad_suscripcion_collective_billing_grouped_refund_chunk(chunk):
        return 3.0
    if is_movilidad_suscripcion_collective_billing_chunk(chunk):
        return 1.0
    if is_movilidad_suscripcion_individual_payment_change_chunk(chunk):
        return -2.0
    return 0.0


def score_movilidad_suscripcion_individual_financing_intent_alignment(
    chunk: RetrievedChunk,
    *,
    query: str,
) -> float:
    """Return a narrow preference score for individual-financing suscripción prompts."""

    if not query_has_movilidad_suscripcion_individual_financing_intent(query):
        return 0.0
    if is_movilidad_suscripcion_individual_financing_chunk(chunk):
        return 3.0
    if is_movilidad_suscripcion_individual_payment_change_chunk(chunk):
        return 2.0
    if is_movilidad_suscripcion_collective_billing_chunk(chunk):
        return -2.0
    return 0.0


def score_movilidad_suscripcion_collective_billing_intent_alignment(
    chunk: RetrievedChunk,
    *,
    query: str,
) -> float:
    """Return a narrow preference score for collective billing prompts."""

    if not query_has_movilidad_suscripcion_collective_billing_intent(query):
        return 0.0
    if is_movilidad_suscripcion_collective_billing_grouped_refund_chunk(chunk):
        return 2.5
    if is_movilidad_suscripcion_collective_billing_chunk(chunk):
        return 1.0
    if is_movilidad_suscripcion_individual_financing_chunk(chunk):
        return -1.5
    return 0.0


def extract_chunk_body_lead_line(text: str) -> str:
    """Return the first meaningful body line from one chunk."""

    body_surface = build_chunk_body_without_markdown_headings(text)
    for line in body_surface.splitlines():
        stripped_line = line.strip()
        if not stripped_line:
            continue
        normalized_line = stripped_line.lstrip("-•➢* ").strip()
        if normalized_line:
            return normalized_line
    return ""


def score_movilidad_suscripcion_collective_billing_lead_quality(
    chunk: RetrievedChunk,
    *,
    query: str,
) -> float:
    """Return a local lead-quality preference for grouped-refund billing chunks."""

    if not query_has_movilidad_suscripcion_collective_billing_intent(query):
        return 0.0
    if not is_movilidad_suscripcion_collective_billing_grouped_refund_chunk(chunk):
        return 0.0

    lead_line = extract_chunk_body_lead_line(chunk.text)
    if not lead_line:
        return -2.0

    lead_score = 0.0
    if lead_line[0].islower():
        lead_score -= 1.0
    else:
        lead_score += 0.5
    if len(lead_line) >= 48:
        lead_score += 0.25
    return lead_score


def build_movilidad_suscripcion_policy_section_priority_key(
    chunk: RetrievedChunk,
    *,
    query: str,
) -> tuple[float, float, float, float, float, float, float]:
    """Return the deterministic section-ordering key for suscripción policy prioritization."""

    return (
        score_movilidad_suscripcion_individual_financing_intent_alignment(chunk, query=query),
        score_movilidad_suscripcion_collective_billing_renewal_intent_alignment(
            chunk,
            query=query,
        ),
        score_movilidad_suscripcion_billing_by_insured_intent_alignment(chunk, query=query),
        score_movilidad_suscripcion_collective_billing_intent_alignment(chunk, query=query),
        score_movilidad_suscripcion_collective_billing_lead_quality(chunk, query=query),
        score_movilidad_suscripcion_evidence_richness(chunk),
        chunk.score,
    )


def build_movilidad_suscripcion_policy_duplicate_resolution_key(
    chunk: RetrievedChunk,
    *,
    query: str,
) -> tuple[float, float, float, float, float, int]:
    """Return the deterministic duplicate-resolution key for suscripción chunks."""

    chunk_index = chunk.chunk_index if isinstance(chunk.chunk_index, int) else 10**9
    section_key = build_movilidad_suscripcion_policy_section_priority_key(
        chunk,
        query=query,
    )
    return (*section_key, -chunk_index)


def count_bullet_lines(text: str) -> int:
    """Return the number of bullet-style lines in one chunk surface."""

    return sum(1 for line in text.splitlines() if line.lstrip().startswith("- "))


def score_movilidad_pv_benefit_breadth(chunk: RetrievedChunk) -> float:
    """Return a deterministic breadth preference for PV benefit sections."""

    total_score = 0.0
    bullet_count = count_bullet_lines(chunk.text)
    total_score += min(bullet_count * 0.45, 2.25)

    normalized_text = normalize_equivalence_text(chunk.text)
    if len(normalized_text) >= 180:
        total_score += 0.40
    if len(normalized_text) >= 320:
        total_score += 0.35

    repeated_section_heading_count = 0
    if chunk.section:
        normalized_section = normalize_equivalence_text(chunk.section)
        repeated_section_heading_count = normalized_text.count(normalized_section)
    if repeated_section_heading_count >= 2:
        total_score -= 0.25

    return total_score


def score_explicit_coverage_chunk_descriptiveness(chunk: RetrievedChunk) -> float:
    """Return a local preference score for descriptive coverage chunks."""

    normalized_text = normalize_equivalence_text(chunk.text)
    total_score = 0.0
    for opener in DESCRIPTIVE_COVERAGE_OPENERS:
        if opener in normalized_text:
            total_score += 2.0
    for opener in OPERATIONAL_COVERAGE_OPENERS:
        if opener in normalized_text:
            total_score -= 1.25
    if "## " in chunk.text:
        total_score += 0.25
    return total_score


def diversify_explicit_coverage_sections(
    ranked_chunks: Sequence[RetrievedChunk],
    *,
    top_k: int,
) -> list[RetrievedChunk]:
    """Prefer breadth across explicit coverage sections before duplicates."""

    if top_k < 1:
        return []

    best_by_section: dict[tuple[str, ...], RetrievedChunk] = {}
    section_order: list[tuple[str, ...]] = []
    remaining_chunks: list[RetrievedChunk] = []

    for chunk in ranked_chunks:
        label_surface = "\n".join(
            value
            for value in (chunk.document_name, chunk.section, *chunk.section_path)
            if value
        )
        if not label_surface_has_explicit_coverage_section(label_surface):
            remaining_chunks.append(chunk)
            continue
        section_id = coverage_section_identity(chunk)
        existing_chunk = best_by_section.get(section_id)
        if existing_chunk is None:
            best_by_section[section_id] = chunk
            section_order.append(section_id)
            continue
        candidate_key = (
            score_explicit_coverage_chunk_descriptiveness(chunk),
            chunk.score,
        )
        existing_key = (
            score_explicit_coverage_chunk_descriptiveness(existing_chunk),
            existing_chunk.score,
        )
        if candidate_key > existing_key:
            remaining_chunks.append(existing_chunk)
            best_by_section[section_id] = chunk
            continue
        remaining_chunks.append(chunk)

    prioritized_coverage_chunks = sorted(
        (best_by_section[section_id] for section_id in section_order),
        key=lambda chunk: (
            build_section_sort_key(chunk.section),
            -score_explicit_coverage_chunk_descriptiveness(chunk),
            -chunk.score,
        ),
    )

    final_chunks: list[RetrievedChunk] = []
    seen_chunk_ids: set[str] = set()
    for chunk in (*prioritized_coverage_chunks, *ranked_chunks, *remaining_chunks):
        if chunk.chunk_id in seen_chunk_ids:
            continue
        final_chunks.append(chunk)
        seen_chunk_ids.add(chunk.chunk_id)
        if len(final_chunks) >= top_k:
            break
    return final_chunks


def diversify_movilidad_pv_benefit_sections(
    ranked_chunks: Sequence[RetrievedChunk],
    *,
    top_k: int,
) -> list[RetrievedChunk]:
    """Prefer broader distinct PV benefit sections before repeated sections."""

    if top_k < 1:
        return []

    best_by_section: dict[tuple[str, ...], RetrievedChunk] = {}
    section_order: list[tuple[str, ...]] = []
    remaining_chunks: list[RetrievedChunk] = []

    for chunk in ranked_chunks:
        if not is_movilidad_pv_document_family_chunk(chunk):
            remaining_chunks.append(chunk)
            continue
        section_id = coverage_section_identity(chunk)
        existing_chunk = best_by_section.get(section_id)
        if existing_chunk is None:
            best_by_section[section_id] = chunk
            section_order.append(section_id)
            continue
        candidate_key = (score_movilidad_pv_benefit_breadth(chunk), chunk.score)
        existing_key = (
            score_movilidad_pv_benefit_breadth(existing_chunk),
            existing_chunk.score,
        )
        if candidate_key > existing_key:
            remaining_chunks.append(existing_chunk)
            best_by_section[section_id] = chunk
            continue
        remaining_chunks.append(chunk)

    prioritized_pv_chunks = sorted(
        (best_by_section[section_id] for section_id in section_order),
        key=lambda chunk: (score_movilidad_pv_benefit_breadth(chunk), chunk.score),
        reverse=True,
    )

    final_chunks: list[RetrievedChunk] = []
    seen_chunk_ids: set[str] = set()
    seen_pv_section_ids: set[tuple[str, ...]] = set()
    for chunk in (*prioritized_pv_chunks, *ranked_chunks, *remaining_chunks):
        if chunk.chunk_id in seen_chunk_ids:
            continue
        if is_movilidad_pv_document_family_chunk(chunk):
            section_id = coverage_section_identity(chunk)
            if section_id in seen_pv_section_ids:
                continue
            seen_pv_section_ids.add(section_id)
        final_chunks.append(chunk)
        seen_chunk_ids.add(chunk.chunk_id)
        if len(final_chunks) >= top_k:
            break
    return final_chunks


def prioritize_movilidad_suscripcion_policy_evidence(
    ranked_chunks: Sequence[RetrievedChunk],
    *,
    query: str,
    top_k: int,
) -> list[RetrievedChunk]:
    """Prefer richer and broader suscripción policy chunks ahead of duplicates."""

    if top_k < 1:
        return []

    best_by_section: dict[tuple[str, ...], RetrievedChunk] = {}
    section_order: list[tuple[str, ...]] = []
    deferred_duplicate_chunks: list[RetrievedChunk] = []
    remaining_chunks: list[RetrievedChunk] = []

    for chunk in ranked_chunks:
        if not is_movilidad_suscripcion_document_family_chunk(chunk):
            remaining_chunks.append(chunk)
            continue
        section_id = coverage_section_identity(chunk)
        existing_chunk = best_by_section.get(section_id)
        if existing_chunk is None:
            best_by_section[section_id] = chunk
            section_order.append(section_id)
            continue
        candidate_key = build_movilidad_suscripcion_policy_duplicate_resolution_key(
            chunk,
            query=query,
        )
        existing_key = build_movilidad_suscripcion_policy_duplicate_resolution_key(
            existing_chunk,
            query=query,
        )
        if candidate_key > existing_key:
            deferred_duplicate_chunks.append(existing_chunk)
            best_by_section[section_id] = chunk
            continue
        deferred_duplicate_chunks.append(chunk)

    prioritized_suscripcion_chunks = sorted(
        (best_by_section[section_id] for section_id in section_order),
        key=lambda chunk: build_movilidad_suscripcion_policy_section_priority_key(
            chunk,
            query=query,
        ),
        reverse=True,
    )

    final_chunks: list[RetrievedChunk] = []
    seen_chunk_ids: set[str] = set()
    for chunk in (
        *prioritized_suscripcion_chunks,
        *deferred_duplicate_chunks,
        *remaining_chunks,
    ):
        if chunk.chunk_id in seen_chunk_ids:
            continue
        final_chunks.append(chunk)
        seen_chunk_ids.add(chunk.chunk_id)
        if len(final_chunks) >= top_k:
            break
    return final_chunks


def build_candidate_pool_limit(
    *,
    query: str,
    top_k: int,
    matched_expansion_rules: Sequence[object],
) -> int:
    """Return the Qdrant candidate-pool limit for one retrieval query."""

    if not matched_expansion_rules:
        if query_has_arl_remuneration_policy_intent(query):
            return min(max(top_k * 3, top_k + 6), 20)
        if (
            query_has_movilidad_suscripcion_policy_intent(query)
            or query_has_movilidad_suscripcion_collective_billing_intent(query)
            or query_has_movilidad_suscripcion_billing_by_insured_intent(query)
            or query_has_movilidad_suscripcion_collective_billing_renewal_intent(query)
            or query_has_movilidad_suscripcion_individual_financing_intent(query)
        ):
            return min(max(top_k * 3, top_k + 6), 20)
        return top_k
    return min(max(top_k * 3, top_k + 4), 20)


def rerank_chunks_for_query_expansion_rules(
    chunks: Sequence[RetrievedChunk],
    *,
    query: str,
    matched_expansion_rules: Sequence[object],
    top_k: int,
) -> list[RetrievedChunk]:
    """Apply deterministic lexical reranking based on matched curated expansion rules."""

    if not matched_expansion_rules:
        ranked_chunks = list(chunks)
        if query_has_arl_remuneration_policy_intent(query):
            return prioritize_arl_remuneration_policy_evidence(
                ranked_chunks,
                query=query,
                top_k=top_k,
            )
        if (
            query_has_movilidad_suscripcion_policy_intent(query)
            or query_has_movilidad_suscripcion_collective_billing_intent(query)
            or query_has_movilidad_suscripcion_billing_by_insured_intent(query)
            or query_has_movilidad_suscripcion_collective_billing_renewal_intent(query)
            or query_has_movilidad_suscripcion_individual_financing_intent(query)
        ):
            return prioritize_movilidad_suscripcion_policy_evidence(
                ranked_chunks,
                query=query,
                top_k=top_k,
            )
        return ranked_chunks[:top_k]

    reranked_candidates: list[tuple[float, int, RetrievedChunk]] = []
    deductible_intent = query_contains_equivalent_phrase(query, "deducible")
    coverage_intent = any(
        query_contains_equivalent_phrase(query, phrase)
        for phrase in QUERY_COVERAGE_INTENT_PHRASES
    )
    for index, chunk in enumerate(chunks):
        score_bonus = 0.0
        section_labels = [
            section_label
            for section_label in (chunk.section, *chunk.section_path)
            if section_label
        ]
        label_surface = "\n".join(
            value
            for value in (chunk.document_name, chunk.section, *chunk.section_path)
            if value
        )
        body_surface = chunk.text
        for matched_rule in matched_expansion_rules:
            for term in matched_rule.append_terms:
                if any(
                    query_contains_equivalent_phrase(section_label, term)
                    for section_label in section_labels
                ):
                    exact_match_token_count = len(tokenize_lexical_surface(term))
                    if query_contains_equivalent_phrase(term, "qué cubre este seguro"):
                        score_bonus += 1.45
                    elif exact_match_token_count >= 5:
                        score_bonus += 0.60
                    else:
                        score_bonus += 0.18
                elif query_contains_equivalent_phrase(label_surface, term):
                    score_bonus += 0.12
                elif query_contains_equivalent_phrase(body_surface, term):
                    score_bonus += 0.04
        if deductible_intent and query_contains_equivalent_phrase(label_surface, "deducible"):
            score_bonus += 0.35
        if coverage_intent and label_surface_has_explicit_coverage_section(label_surface):
            score_bonus += 0.30
        reranked_candidates.append(
            (
                chunk.score + score_bonus,
                -index,
                chunk.model_copy(update={"score": chunk.score + score_bonus}),
            )
        )

    reranked_candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    ranked_chunks = [candidate[2] for candidate in reranked_candidates]
    if coverage_intent:
        return diversify_explicit_coverage_sections(ranked_chunks, top_k=top_k)
    if query_has_movilidad_pv_benefit_intent(query):
        return diversify_movilidad_pv_benefit_sections(ranked_chunks, top_k=top_k)
    if query_has_arl_remuneration_policy_intent(query):
        return prioritize_arl_remuneration_policy_evidence(
            ranked_chunks,
            query=query,
            top_k=top_k,
        )
    if (
        query_has_movilidad_suscripcion_policy_intent(query)
        or query_has_movilidad_suscripcion_collective_billing_intent(query)
        or query_has_movilidad_suscripcion_billing_by_insured_intent(query)
        or query_has_movilidad_suscripcion_collective_billing_renewal_intent(query)
        or query_has_movilidad_suscripcion_individual_financing_intent(query)
    ):
        return prioritize_movilidad_suscripcion_policy_evidence(
            ranked_chunks,
            query=query,
            top_k=top_k,
        )
    return ranked_chunks[:top_k]


def select_answer_evidence_chunks(
    retrieved_chunks: Sequence[RetrievedChunk],
    *,
    query: str,
    min_retrieval_chunks_for_high_confidence: int,
) -> list[RetrievedChunk]:
    """Return the answer-facing evidence subset for one retrieval query."""

    ranked_chunks = list(retrieved_chunks)
    if not query_has_movilidad_suscripcion_individual_financing_intent(query):
        return ranked_chunks

    direct_financing_chunks = [
        chunk
        for chunk in ranked_chunks
        if is_movilidad_suscripcion_direct_financing_support_chunk(chunk)
    ]
    if len(direct_financing_chunks) < min_retrieval_chunks_for_high_confidence:
        return ranked_chunks
    return direct_financing_chunks


def query_has_arl_commissions_guide_intent(query: str) -> bool:
    """Return whether one query explicitly targets the ARL commissions guide."""

    normalized_query = normalize_equivalence_text(query)
    return (
        "arl" in normalized_query
        and "comision" in normalized_query
        and any(
            phrase in normalized_query
            for phrase in ("consulto", "consultar", "consulta", "liquidacion", "liquidar")
        )
    )


def is_arl_commissions_guide_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk belongs to the ARL commissions guide family."""

    if chunk.product != "arl" or chunk.document_type != "guide":
        return False
    normalized_document_name = normalize_equivalence_text(chunk.document_name)
    normalized_source_id = normalize_equivalence_text(chunk.source_pdf_id)
    return (
        "consulta liquidacion de comisiones" in normalized_document_name
        or "instructivos-consulta-de-comisiones-arl-sura" in normalized_source_id
    )


def query_has_arl_account_update_guide_intent(query: str) -> bool:
    """Return whether one query explicitly targets the ARL account-update guide."""

    normalized_query = normalize_equivalence_text(query)
    return (
        "arl" in normalized_query
        and "cuenta bancaria" in normalized_query
        and any(
            phrase in normalized_query
            for phrase in (
                "actualizo",
                "actualizar",
                "actualizacion",
                "pago de comisiones",
            )
        )
    )


def is_arl_account_update_guide_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk belongs to the ARL account-update guide family."""

    if chunk.product != "arl" or chunk.document_type != "guide":
        return False
    normalized_document_name = normalize_equivalence_text(chunk.document_name)
    normalized_source_id = normalize_equivalence_text(chunk.source_pdf_id)
    return (
        "actualizacion de cuenta bancaria" in normalized_document_name
        or "instructivos-actualizacion-cuenta-bancaria-v2" in normalized_source_id
    )


def query_has_arl_rui_normativity_intent(query: str) -> bool:
    """Return whether one query explicitly asks for ARL/RUI normativity."""

    normalized_query = normalize_equivalence_text(query)
    return (
        "normatividad" in normalized_query
        and (
            "rui" in normalized_query
            or "registro unico" in normalized_query
            or "intermediario" in normalized_query
        )
    )


def is_arl_rui_normativity_support_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk directly supports ARL/RUI normativity answers."""

    if chunk.product != "arl" or chunk.document_type != "faq":
        return False
    if "registro-unico-de-intermediacion-rui" not in chunk.source_pdf_id:
        return False
    normalized_section = normalize_equivalence_text(chunk.section or "")
    if "cual es la normatividad que rige el registro unico de intermediarios" in normalized_section:
        return True
    normalized_text = normalize_equivalence_text(chunk.text)
    matching_anchors = sum(1 for anchor in ARL_RUI_NORMATIVE_ANCHORS if anchor in normalized_text)
    return matching_anchors >= 2


def select_citation_evidence_chunks(
    retrieved_chunks: Sequence[RetrievedChunk],
    *,
    query: str,
) -> list[RetrievedChunk]:
    """Return the narrower citation/doc-basis subset for one answer query."""

    citation_chunks = list(retrieved_chunks)
    if query_has_arl_remuneration_overview_intent(query):
        direct_remuneration_overview_chunks = [
            chunk
            for chunk in citation_chunks
            if is_arl_remuneration_overview_citation_support_chunk(chunk)
        ]
        if direct_remuneration_overview_chunks:
            return direct_remuneration_overview_chunks
    if query_has_arl_account_update_guide_intent(query):
        direct_account_update_chunks = [
            chunk for chunk in citation_chunks if is_arl_account_update_guide_chunk(chunk)
        ]
        if direct_account_update_chunks:
            return direct_account_update_chunks
    if query_has_arl_commissions_guide_intent(query):
        direct_commissions_chunks = [
            chunk for chunk in citation_chunks if is_arl_commissions_guide_chunk(chunk)
        ]
        if direct_commissions_chunks:
            return direct_commissions_chunks
    if not query_has_arl_rui_normativity_intent(query):
        return citation_chunks

    direct_normativity_chunks = [
        chunk for chunk in citation_chunks if is_arl_rui_normativity_support_chunk(chunk)
    ]
    if direct_normativity_chunks:
        return direct_normativity_chunks
    return citation_chunks
