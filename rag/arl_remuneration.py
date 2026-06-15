"""ARL remuneration-policy retrieval helpers."""

from __future__ import annotations

from collections.abc import Sequence

from contracts import RetrievedChunk
from rag.term_equivalences import normalize_equivalence_text

ARL_REMUNERATION_POLICY_INTENT_PHRASES = (
    "remuneracion",
    "esquema de remuneracion",
    "esquema remuneracion",
    "comision",
    "comisiones",
    "pago de comisiones",
    "pago de comision",
)

ARL_REMUNERATION_POLICY_SECTION_BONUSES: tuple[tuple[str, float], ...] = (
    ("pago de comisiones por atraccion", 3.2),
    ("clientes nuevos (venta) para el canal externo", 2.8),
    ("clientes nuevos (venta) del canal externo", 2.8),
    ("requisitos indispensables para el pago de comision", 2.2),
    ("por cambio de intermediario", 1.9),
    ("politica de designacion de intermediarios", 1.6),
    ("apetito comercial por grupos clientes nuevos (venta) para el canal externo", 1.2),
)

ARL_REMUNERATION_POLICY_INTRO_SECTION_PENALTIES: tuple[tuple[str, float], ...] = (
    ("canales para la afiliacion a arl sura", -2.4),
    ("canal externo", -1.6),
)

ARL_REMUNERATION_POLICY_OVERVIEW_SECTION_ANCHORS = (
    "clientes nuevos (venta) para el canal externo",
    "clientes nuevos (venta) del canal externo",
)

ARL_REMUNERATION_POLICY_APPETITE_SECTION_ANCHORS = (
    "apetito comercial por grupos clientes nuevos (venta) para el canal externo",
)

ARL_REMUNERATION_POLICY_TABLE_SECTION_ANCHORS = (
    "pago de comisiones por atraccion",
)

ARL_REMUNERATION_POLICY_CHANGE_INTERMEDIARY_SECTION_ANCHORS = (
    "por cambio de intermediario",
)


def _count_bullet_lines(text: str) -> int:
    """Return the number of bullet-style lines in one chunk surface."""

    return sum(1 for line in text.splitlines() if line.lstrip().startswith("- "))


def _coverage_section_identity(chunk: RetrievedChunk) -> tuple[str, ...]:
    """Return a stable identity for coverage-section diversification."""

    if chunk.section_path:
        return tuple(chunk.section_path)
    if chunk.section:
        return (chunk.section,)
    return (chunk.chunk_id,)


def _build_label_surface(chunk: RetrievedChunk) -> str:
    """Return the normalized label surface for one retrieved chunk."""

    return normalize_equivalence_text(
        "\n".join(
            value
            for value in (
                chunk.document_name,
                chunk.section,
                *chunk.section_path,
            )
            if value
        )
    )


def query_has_arl_remuneration_policy_intent(query: str) -> bool:
    """Return whether one query broadly targets the ARL remuneration policy."""

    normalized_query = normalize_equivalence_text(query)
    if "arl" not in normalized_query:
        return False
    if not any(
        phrase in normalized_query for phrase in ARL_REMUNERATION_POLICY_INTENT_PHRASES
    ):
        return False
    return any(
        anchor in normalized_query
        for anchor in (
            "canal externo",
            "intermediario",
            "intermediarios",
            "atraccion",
            "clientes nuevos",
        )
    ) or "esquema" in normalized_query


def query_has_arl_remuneration_table_intent(query: str) -> bool:
    """Return whether one ARL remuneration query explicitly asks for tables or percentages."""

    if not query_has_arl_remuneration_policy_intent(query):
        return False

    normalized_query = normalize_equivalence_text(query)
    return any(
        phrase in normalized_query
        for phrase in (
            "porcentaje",
            "porcentajes",
            "%",
            "sector economico",
            "sectores",
            "tabla",
            "tablas",
            "comision por sector",
            "comisiones por sector",
            "1a",
            "1b",
            "3a",
            "3b",
        )
    )


def query_has_arl_remuneration_overview_intent(query: str) -> bool:
    """Return whether one ARL remuneration query is broad and overview-seeking."""

    if not query_has_arl_remuneration_policy_intent(query):
        return False
    if query_has_arl_remuneration_table_intent(query):
        return False

    normalized_query = normalize_equivalence_text(query)
    return any(
        phrase in normalized_query
        for phrase in (
            "esquema",
            "como funciona",
            "como opera",
            "como es",
            "remuneracion",
            "comisiones",
            "explicame",
            "explicacion",
        )
    )


def is_arl_remuneration_policy_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk belongs to the ARL remuneration-policy family."""

    if chunk.product != "arl" or chunk.document_type != "policy":
        return False
    normalized_document_name = normalize_equivalence_text(chunk.document_name)
    normalized_source_id = normalize_equivalence_text(chunk.source_pdf_id)
    return (
        "esquema remuneracion" in normalized_document_name
        or "politica-de-remuneracion-canal-externo" in normalized_source_id
    )


def score_arl_remuneration_policy_intent_alignment(
    chunk: RetrievedChunk,
    *,
    query: str,
) -> float:
    """Return a narrow preference score for broad ARL remuneration-policy prompts."""

    if not query_has_arl_remuneration_policy_intent(query):
        return 0.0
    if not is_arl_remuneration_policy_chunk(chunk):
        return 0.0

    normalized_label_surface = _build_label_surface(chunk)
    total_score = 0.0
    for phrase, bonus in ARL_REMUNERATION_POLICY_SECTION_BONUSES:
        if phrase in normalized_label_surface:
            total_score += bonus
    for phrase, penalty in ARL_REMUNERATION_POLICY_INTRO_SECTION_PENALTIES:
        if phrase in normalized_label_surface:
            total_score += penalty
    if chunk.section and normalize_equivalence_text(chunk.section) == normalize_equivalence_text(
        chunk.document_name
    ):
        total_score -= 2.0
    return total_score


def score_arl_remuneration_policy_evidence_richness(chunk: RetrievedChunk) -> float:
    """Return a deterministic local preference for richer remuneration chunks."""

    if not is_arl_remuneration_policy_chunk(chunk):
        return 0.0

    normalized_text = normalize_equivalence_text(chunk.text)
    total_score = 0.0
    if "% comision" in normalized_text:
        total_score += 1.4
    if "|" in chunk.text:
        total_score += 1.0
    if _count_bullet_lines(chunk.text) >= 2:
        total_score += 0.65
    if "clientes nuevos" in normalized_text:
        total_score += 0.45
    if "cambio de intermediario" in normalized_text:
        total_score += 0.40
    if len(normalized_text) >= 260:
        total_score += 0.25
    return total_score


def score_arl_remuneration_policy_overview_vs_table_priority(
    chunk: RetrievedChunk,
    *,
    query: str,
) -> float:
    """Return a narrow preference for overview-first or table-first ARL evidence."""

    if not is_arl_remuneration_policy_chunk(chunk):
        return 0.0

    normalized_label_surface = _build_label_surface(chunk)
    overview_chunk = any(
        anchor in normalized_label_surface
        for anchor in ARL_REMUNERATION_POLICY_OVERVIEW_SECTION_ANCHORS
    )
    table_chunk = any(
        anchor in normalized_label_surface
        for anchor in ARL_REMUNERATION_POLICY_TABLE_SECTION_ANCHORS
    )

    total_score = 0.0
    if query_has_arl_remuneration_overview_intent(query):
        if overview_chunk:
            total_score += 3.6
        if table_chunk:
            total_score -= 2.1
        if chunk.section and normalize_equivalence_text(chunk.section) in {
            *ARL_REMUNERATION_POLICY_APPETITE_SECTION_ANCHORS,
        }:
            total_score -= 1.2
        if "|" in chunk.text:
            total_score -= 0.45
    elif query_has_arl_remuneration_table_intent(query):
        if table_chunk:
            total_score += 2.6
        if overview_chunk:
            total_score -= 0.4
        if "|" in chunk.text:
            total_score += 0.75

    return total_score


def is_arl_remuneration_overview_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk is the explanatory ARL remuneration overview."""

    if not is_arl_remuneration_policy_chunk(chunk):
        return False
    normalized_section = normalize_equivalence_text(chunk.section or "")
    return normalized_section in ARL_REMUNERATION_POLICY_OVERVIEW_SECTION_ANCHORS


def is_arl_remuneration_table_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk belongs to the remuneration table family."""

    if not is_arl_remuneration_policy_chunk(chunk):
        return False
    normalized_label_surface = _build_label_surface(chunk)
    return any(
        anchor in normalized_label_surface
        for anchor in ARL_REMUNERATION_POLICY_TABLE_SECTION_ANCHORS
    )


def is_arl_remuneration_appetite_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk belongs to the appetite/grouping support family."""

    if not is_arl_remuneration_policy_chunk(chunk):
        return False
    normalized_section = normalize_equivalence_text(chunk.section or "")
    return normalized_section in ARL_REMUNERATION_POLICY_APPETITE_SECTION_ANCHORS


def is_arl_remuneration_change_intermediary_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk directly covers change-of-intermediary rules."""

    if not is_arl_remuneration_policy_chunk(chunk):
        return False
    normalized_label_surface = _build_label_surface(chunk)
    return any(
        anchor in normalized_label_surface
        for anchor in ARL_REMUNERATION_POLICY_CHANGE_INTERMEDIARY_SECTION_ANCHORS
    )


def is_arl_remuneration_overview_citation_support_chunk(chunk: RetrievedChunk) -> bool:
    """Return whether one chunk directly supports broad ARL remuneration overviews."""

    return any(
        matcher(chunk)
        for matcher in (
            is_arl_remuneration_overview_chunk,
            is_arl_remuneration_appetite_chunk,
            is_arl_remuneration_table_chunk,
            is_arl_remuneration_change_intermediary_chunk,
        )
    )


def build_arl_remuneration_policy_priority_key(
    chunk: RetrievedChunk,
    *,
    query: str,
) -> tuple[float, float, float, float]:
    """Return the deterministic ranking key for ARL remuneration-policy chunks."""

    return (
        score_arl_remuneration_policy_intent_alignment(chunk, query=query),
        score_arl_remuneration_policy_overview_vs_table_priority(
            chunk,
            query=query,
        ),
        score_arl_remuneration_policy_evidence_richness(chunk),
        chunk.score,
    )


def prioritize_arl_remuneration_policy_evidence(
    ranked_chunks: Sequence[RetrievedChunk],
    *,
    query: str,
    top_k: int,
) -> list[RetrievedChunk]:
    """Prefer explicit ARL remuneration sections ahead of intro policy chunks."""

    if top_k < 1:
        return []

    best_by_section: dict[tuple[str, ...], RetrievedChunk] = {}
    section_order: list[tuple[str, ...]] = []
    deferred_duplicate_chunks: list[RetrievedChunk] = []
    remaining_chunks: list[RetrievedChunk] = []

    for chunk in ranked_chunks:
        if not is_arl_remuneration_policy_chunk(chunk):
            remaining_chunks.append(chunk)
            continue
        section_id = _coverage_section_identity(chunk)
        existing_chunk = best_by_section.get(section_id)
        if existing_chunk is None:
            best_by_section[section_id] = chunk
            section_order.append(section_id)
            continue
        candidate_key = build_arl_remuneration_policy_priority_key(chunk, query=query)
        existing_key = build_arl_remuneration_policy_priority_key(existing_chunk, query=query)
        if candidate_key > existing_key:
            deferred_duplicate_chunks.append(existing_chunk)
            best_by_section[section_id] = chunk
            continue
        deferred_duplicate_chunks.append(chunk)

    prioritized_chunks = sorted(
        (best_by_section[section_id] for section_id in section_order),
        key=lambda chunk: build_arl_remuneration_policy_priority_key(chunk, query=query),
        reverse=True,
    )

    forced_lead_chunks: list[RetrievedChunk] = []
    if query_has_arl_remuneration_overview_intent(query):
        overview_candidates = [
            chunk for chunk in prioritized_chunks if is_arl_remuneration_overview_chunk(chunk)
        ]
        if overview_candidates:
            forced_lead_chunks.append(
                max(
                    overview_candidates,
                    key=lambda chunk: build_arl_remuneration_policy_priority_key(
                        chunk,
                        query=query,
                    ),
                )
            )
    elif query_has_arl_remuneration_table_intent(query):
        table_candidates = [
            chunk for chunk in prioritized_chunks if is_arl_remuneration_table_chunk(chunk)
        ]
        if table_candidates:
            forced_lead_chunks.append(
                max(
                    table_candidates,
                    key=lambda chunk: build_arl_remuneration_policy_priority_key(
                        chunk,
                        query=query,
                    ),
                )
            )

    final_chunks: list[RetrievedChunk] = []
    seen_chunk_ids: set[str] = set()
    for chunk in (
        *forced_lead_chunks,
        *prioritized_chunks,
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
