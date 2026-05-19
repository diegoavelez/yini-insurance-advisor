"""Independently callable clause extraction tool wrapper."""

from __future__ import annotations

import logging
import re
from collections.abc import Sequence

from contracts import (
    Clause,
    ClauseExtractionResult,
    ClauseExtractionToolResult,
    RetrievedChunk,
    ToolError,
)
from ops.observability import log_timed_event

TOOL_LOGGER = logging.getLogger("yini.tools.clause_extraction")
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")


def classify_clause_tool_error(exc: Exception) -> ToolError:
    """Map clause extraction failures into the typed tool error surface."""

    if isinstance(exc, ValueError):
        return ToolError(kind="input_validation_failure", message=str(exc))
    return ToolError(kind="extraction_failure", message=str(exc))


def categorize_clause(text: str) -> str | None:
    """Return the existing clause category conservatively from chunk text."""

    normalized_text = text.lower()
    if any(
        token in normalized_text
        for token in ("excluded", "exclusion", "no cubre", "not covered")
    ):
        return "exclusion"
    if any(token in normalized_text for token in ("except", "exception", "unless")):
        return "exception"
    if any(
        token in normalized_text
        for token in ("must", "required", "requirement", "shall", "debe")
    ):
        return "requirement"
    if any(
        token in normalized_text
        for token in ("procedure", "submit", "report", "notify", "process")
    ):
        return "procedure"
    if any(
        token in normalized_text
        for token in ("restricted", "restriction", "limited to", "subject to")
    ):
        return "restriction"
    if any(token in normalized_text for token in ("coverage", "covered", "covers", "cubre")):
        return "coverage"
    return None


def summarize_clause_text(text: str) -> str:
    """Return one conservative summary sentence from clause text."""

    stripped_text = " ".join(text.split())
    sentence = SENTENCE_SPLIT_PATTERN.split(stripped_text, maxsplit=1)[0]
    return sentence[:280]


def extract_clause_from_chunk(chunk: RetrievedChunk) -> Clause | None:
    """Extract one conservative clause from a retrieved chunk when category is clear."""

    category = categorize_clause(chunk.text)
    if category is None:
        return None
    return Clause(
        category=category,
        summary=summarize_clause_text(chunk.text),
        document_name=chunk.document_name,
        page=chunk.page,
        section=chunk.section,
        clause_id=chunk.clause_id,
        supporting_chunk_ids=[chunk.chunk_id],
    )


def validate_clause_extraction_input(retrieved_chunks: Sequence[RetrievedChunk]) -> None:
    """Validate clause extraction input before processing."""

    if not isinstance(retrieved_chunks, Sequence):
        raise ValueError("retrieved_chunks must be a sequence of RetrievedChunk items.")
    for chunk in retrieved_chunks:
        if not isinstance(chunk, RetrievedChunk):
            raise ValueError("retrieved_chunks must contain only RetrievedChunk items.")


def clause_extraction_tool(
    retrieved_chunks: Sequence[RetrievedChunk],
    *,
    request_id: str | None = None,
) -> ClauseExtractionToolResult:
    """Extract typed clauses from retrieved evidence only."""

    try:
        with log_timed_event(
            TOOL_LOGGER,
            event_type="clause_extraction_tool",
            request_id=request_id,
            start_fields={"input_chunk_count": len(retrieved_chunks)},
            success_fields_factory=(
                lambda _duration_ms: {"result_count": len(clause_result.clauses)}
            ),
        ):
            validate_clause_extraction_input(retrieved_chunks)
            clause_result = ClauseExtractionResult(
                clauses=[
                    clause
                    for chunk in retrieved_chunks
                    for clause in [extract_clause_from_chunk(chunk)]
                    if clause is not None
                ]
            )
            return ClauseExtractionToolResult(ok=True, result=clause_result)
    except Exception as exc:
        return ClauseExtractionToolResult(ok=False, error=classify_clause_tool_error(exc))
