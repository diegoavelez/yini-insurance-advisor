"""Independently callable response draft tool wrapper."""

from __future__ import annotations

import logging
from collections.abc import Sequence

from contracts import (
    AdvisorDraftResponse,
    Citation,
    DocumentaryBasisItem,
    GroundingVerification,
    PolicyComparisonResult,
    ResponseDraftToolResult,
    ToolError,
)
from ops.observability import log_timed_event

TOOL_LOGGER = logging.getLogger("yini.tools.response_draft")
ADVISOR_REVIEW_NOTICE = "This response is a draft for advisor review."


def classify_response_draft_error(exc: Exception) -> ToolError:
    """Map response drafting failures into the typed tool error surface."""

    if isinstance(exc, ValueError):
        return ToolError(kind="input_validation_failure", message=str(exc))
    return ToolError(kind="drafting_failure", message=str(exc))


def validate_response_draft_input(
    user_query: str,
    documentary_basis: Sequence[DocumentaryBasisItem],
    citations: Sequence[Citation],
    verification: GroundingVerification | None,
    comparison_result: PolicyComparisonResult | None,
) -> None:
    """Validate response drafting inputs before processing."""

    if not isinstance(user_query, str) or not user_query.strip():
        raise ValueError("user_query must be a non-empty string.")
    if not isinstance(documentary_basis, Sequence):
        raise ValueError("documentary_basis must be a sequence of DocumentaryBasisItem items.")
    if not isinstance(citations, Sequence):
        raise ValueError("citations must be a sequence of Citation items.")
    for basis_item in documentary_basis:
        if not isinstance(basis_item, DocumentaryBasisItem):
            raise ValueError(
                "documentary_basis must contain only DocumentaryBasisItem items."
            )
    for citation in citations:
        if not isinstance(citation, Citation):
            raise ValueError("citations must contain only Citation items.")
    if verification is not None and not isinstance(verification, GroundingVerification):
        raise ValueError("verification must be a GroundingVerification item when provided.")
    if comparison_result is not None and not isinstance(
        comparison_result,
        PolicyComparisonResult,
    ):
        raise ValueError(
            "comparison_result must be a PolicyComparisonResult item when provided."
        )


def build_insufficient_draft_response(
    *,
    citations: Sequence[Citation],
    documentary_basis: Sequence[DocumentaryBasisItem],
    limitations: list[str],
) -> AdvisorDraftResponse:
    """Build the valid non-error drafting output for insufficient information."""

    return AdvisorDraftResponse(
        suggested_answer=(
            "I do not have enough grounded, verified evidence to produce a strong advisor "
            "draft response."
        ),
        documentary_basis=list(documentary_basis),
        citations=list(citations),
        confidence="low",
        limitations=limitations,
        advisor_review_notice=ADVISOR_REVIEW_NOTICE,
    )


def build_successful_draft_response(
    *,
    user_query: str,
    citations: Sequence[Citation],
    documentary_basis: Sequence[DocumentaryBasisItem],
    verification: GroundingVerification | None,
    comparison_result: PolicyComparisonResult | None,
) -> AdvisorDraftResponse:
    """Build a conservative advisor-facing draft from typed upstream inputs only."""

    confidence = verification.confidence if verification is not None else "medium"
    limitations: list[str] = []
    if verification is not None:
        limitations.extend(verification.unsupported_claims)
        limitations.extend(verification.missing_citations)

    if comparison_result is not None and comparison_result.notes:
        limitations.extend(comparison_result.notes)

    if comparison_result is not None and comparison_result.comparison_points:
        comparison_summary = " ".join(
            point.finding for point in comparison_result.comparison_points
        )
        suggested_answer = (
            f"For the query '{user_query}', the compared policy evidence indicates: "
            f"{comparison_summary}"
        )
    else:
        source_documents = ", ".join(
            sorted({basis_item.document_name for basis_item in documentary_basis})
        )
        suggested_answer = (
            f"For the query '{user_query}', the reviewed evidence from {source_documents} "
            "supports the attached draft guidance."
        )

    if confidence != "high":
        limitations.append(
            "Advisor review is required before relying on this draft response."
        )

    deduped_limitations = list(dict.fromkeys(limitations))
    return AdvisorDraftResponse(
        suggested_answer=suggested_answer,
        documentary_basis=list(documentary_basis),
        citations=list(citations),
        confidence=confidence,
        limitations=deduped_limitations,
        advisor_review_notice=ADVISOR_REVIEW_NOTICE,
    )


def response_draft_tool(
    user_query: str,
    documentary_basis: Sequence[DocumentaryBasisItem],
    citations: Sequence[Citation],
    *,
    verification: GroundingVerification | None = None,
    comparison_result: PolicyComparisonResult | None = None,
    request_id: str | None = None,
) -> ResponseDraftToolResult:
    """Draft an advisor-facing response only from typed upstream inputs."""

    try:
        with log_timed_event(
            TOOL_LOGGER,
            event_type="response_draft_tool",
            request_id=request_id,
            start_fields={
                "documentary_basis_count": len(documentary_basis),
                "citation_count": len(citations),
                "has_verification": verification is not None,
                "has_comparison_result": comparison_result is not None,
            },
            success_fields_factory=(
                lambda _duration_ms: {
                    "confidence": draft_response.confidence,
                    "limitation_count": len(draft_response.limitations),
                }
            ),
        ):
            validate_response_draft_input(
                user_query,
                documentary_basis,
                citations,
                verification,
                comparison_result,
            )

            insufficient_information = (
                not documentary_basis
                or not citations
                or (verification is not None and not verification.supported)
            )
            if insufficient_information:
                limitations = []
                if verification is not None:
                    limitations.extend(verification.unsupported_claims)
                    limitations.extend(verification.missing_citations)
                if not documentary_basis:
                    limitations.append("No documentary basis was provided.")
                if not citations:
                    limitations.append("No citations were provided.")
                limitations = list(
                    dict.fromkeys(
                        limitations
                        or ["Insufficient evidence was provided for a strong draft response."]
                    )
                )
                draft_response = build_insufficient_draft_response(
                    citations=citations,
                    documentary_basis=documentary_basis,
                    limitations=limitations,
                )
                return ResponseDraftToolResult(ok=True, result=draft_response)

            draft_response = build_successful_draft_response(
                user_query=user_query,
                citations=citations,
                documentary_basis=documentary_basis,
                verification=verification,
                comparison_result=comparison_result,
            )
            return ResponseDraftToolResult(ok=True, result=draft_response)
    except Exception as exc:
        return ResponseDraftToolResult(
            ok=False,
            error=classify_response_draft_error(exc),
        )
