from __future__ import annotations

import importlib
import logging

from agents.response_draft_tool import (
    classify_response_draft_error,
    response_draft_tool,
)
from contracts import (
    Citation,
    ComparisonItem,
    DocumentaryBasisItem,
    GroundingVerification,
    PolicyComparisonResult,
)

draft_tool_module = importlib.import_module("agents.response_draft_tool")


def make_basis_item(
    *,
    document_name: str = "Policy A",
    page: int = 4,
    section: str = "Coverage",
    clause_id: str = "1.2",
    note: str = "Derived from chunk policy-a:v2:0000",
) -> DocumentaryBasisItem:
    return DocumentaryBasisItem(
        document_name=document_name,
        page=page,
        section=section,
        clause_id=clause_id,
        note=note,
    )


def make_citation(
    *,
    document_name: str = "Policy A",
    chunk_id: str | None = "policy-a:v2:0000",
    page: int = 4,
    section: str = "Coverage",
    clause_id: str = "1.2",
) -> Citation:
    return Citation(
        document_name=document_name,
        chunk_id=chunk_id,
        page=page,
        section=section,
        clause_id=clause_id,
    )


def make_verification(
    *,
    supported: bool = True,
    confidence: str = "high",
    unsupported_claims: list[str] | None = None,
    missing_citations: list[str] | None = None,
) -> GroundingVerification:
    return GroundingVerification(
        supported=supported,
        confidence=confidence,
        unsupported_claims=unsupported_claims or [],
        missing_citations=missing_citations or [],
    )


def make_comparison_result() -> PolicyComparisonResult:
    return PolicyComparisonResult(
        comparison_points=[
            ComparisonItem(
                criterion="coverage_comparison",
                finding="Coverage language differs across the compared documents.",
                source_documents=["Policy A", "Policy B"],
                sufficient_information=True,
            )
        ],
        sufficient_information=True,
        notes=[],
    )


def make_comparison_result_with_notes() -> PolicyComparisonResult:
    return PolicyComparisonResult(
        comparison_points=[
            ComparisonItem(
                criterion="coverage_comparison",
                finding="Coverage language differs across the compared documents.",
                source_documents=["Policy A", "Policy B"],
                sufficient_information=True,
            )
        ],
        sufficient_information=True,
        notes=["Evidence remains partial for a strong final recommendation."],
    )


def test_response_draft_tool_returns_typed_success() -> None:
    result = response_draft_tool(
        "What coverage applies?",
        [make_basis_item()],
        [make_citation()],
        verification=make_verification(),
        comparison_result=make_comparison_result(),
    )

    assert result.ok is True
    assert result.result is not None
    assert "Coverage language differs" in result.result.suggested_answer
    assert result.result.confidence == "high"
    assert result.result.advisor_review_notice == "This response is a draft for advisor review."


def test_response_draft_tool_downgrades_overconfident_output(caplog) -> None:
    caplog.set_level(logging.INFO)

    result = response_draft_tool(
        "What coverage applies?",
        [make_basis_item()],
        [make_citation()],
        verification=make_verification(confidence="high"),
        comparison_result=make_comparison_result_with_notes(),
        request_id="draft-123456789012",
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.confidence == "medium"
    assert any(
        "confidence was downgraded" in limitation.lower()
        for limitation in result.result.limitations
    )
    guardrail_event = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", "") == "confidence_consistency_guardrail_triggered"
    )
    assert guardrail_event.request_id == "draft-123456789012"
    assert guardrail_event.proposed_confidence == "high"
    assert guardrail_event.surfaced_confidence == "medium"


def test_response_draft_tool_returns_valid_insufficient_information() -> None:
    result = response_draft_tool(
        "What coverage applies?",
        [],
        [],
        verification=make_verification(
            supported=False,
            confidence="low",
            unsupported_claims=["Evidence is insufficient."],
            missing_citations=["No citations were supplied."],
        ),
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.confidence == "low"
    assert result.result.limitations
    assert "not have enough grounded" in result.result.suggested_answer.lower()
    assert result.result.advisor_review_notice == "This response is a draft for advisor review."


def test_response_draft_tool_applies_citation_presence_guardrail(caplog) -> None:
    caplog.set_level(logging.INFO)

    result = response_draft_tool(
        "What coverage applies?",
        [make_basis_item()],
        [],
        verification=make_verification(supported=True, confidence="high"),
        request_id="draft-123456789012",
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.confidence == "low"
    assert result.result.citations == []
    assert any(
        "citations are required" in limitation.lower()
        for limitation in result.result.limitations
    )
    guardrail_event = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", "") == "citation_presence_guardrail_triggered"
    )
    assert guardrail_event.request_id == "draft-123456789012"
    assert guardrail_event.guardrail_surface == "response_draft_tool"


def test_response_draft_output_remains_traceable_to_inputs() -> None:
    basis_item = make_basis_item()
    citation = make_citation()

    result = response_draft_tool(
        "What coverage applies?",
        [basis_item],
        [citation],
        verification=make_verification(),
    )

    assert result.result is not None
    assert result.result.documentary_basis == [basis_item]
    assert result.result.citations == [citation]


def test_response_draft_tool_returns_typed_input_validation_failure() -> None:
    result = response_draft_tool(
        "",
        [make_basis_item()],
        [make_citation()],
    )

    assert result.ok is False
    assert result.error is not None
    assert result.error.kind == "input_validation_failure"


def test_response_draft_tool_failure_remains_observable(caplog) -> None:
    caplog.set_level(logging.INFO)

    original = draft_tool_module.build_successful_draft_response

    def explode(*_args, **_kwargs):
        raise RuntimeError("draft failed")

    draft_tool_module.build_successful_draft_response = explode
    try:
        result = response_draft_tool(
            "What coverage applies?",
            [make_basis_item()],
            [make_citation()],
            verification=make_verification(),
            request_id="draft-123456789012",
        )
    finally:
        draft_tool_module.build_successful_draft_response = original

    assert result.ok is False
    assert result.error is not None
    assert result.error.kind == "drafting_failure"
    failed = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", "") == "response_draft_tool_failed"
    )
    assert failed.request_id == "draft-123456789012"


def test_response_draft_tool_success_preserves_request_correlation(caplog) -> None:
    caplog.set_level(logging.INFO)

    result = response_draft_tool(
        "What coverage applies?",
        [make_basis_item()],
        [make_citation()],
        verification=make_verification(confidence="medium"),
        request_id="draft-123456789012",
    )

    assert result.ok is True
    succeeded = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", "") == "response_draft_tool_succeeded"
    )
    assert succeeded.request_id == "draft-123456789012"
    assert succeeded.duration_ms >= 0


def test_response_draft_tool_reduces_certainty_when_evidence_is_weaker() -> None:
    result = response_draft_tool(
        "What coverage applies?",
        [make_basis_item()],
        [make_citation()],
        verification=make_verification(confidence="medium"),
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.confidence == "medium"
    assert any(
        "advisor review is required" in limitation.lower()
        for limitation in result.result.limitations
    )


def test_classify_response_draft_error_distinguishes_runtime_failure() -> None:
    error = classify_response_draft_error(RuntimeError("draft failed"))

    assert error.kind == "drafting_failure"
