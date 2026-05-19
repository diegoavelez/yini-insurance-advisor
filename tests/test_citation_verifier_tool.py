from __future__ import annotations

import importlib
import logging

from agents.citation_verifier_tool import (
    citation_verifier_tool,
    classify_citation_verifier_error,
)
from contracts import Citation, RetrievedChunk

verifier_module = importlib.import_module("agents.citation_verifier_tool")


def make_chunk(
    *,
    chunk_id: str = "policy-a:v2:0000",
    text: str = "Hospitalization coverage applies for listed emergencies.",
    document_name: str = "Policy A",
    page: int = 4,
    section: str = "Coverage",
    clause_id: str = "1.2",
    score: float = 0.91,
) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=chunk_id,
        text=text,
        document_name=document_name,
        page=page,
        section=section,
        clause_id=clause_id,
        score=score,
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


def test_citation_verifier_tool_returns_structured_success() -> None:
    result = citation_verifier_tool(
        "Hospitalization coverage applies for listed emergencies.",
        [make_citation()],
        [make_chunk()],
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.verification.supported is True
    assert result.result.verification.confidence == "high"
    assert result.result.reviewed_citations[0].chunk_id == "policy-a:v2:0000"


def test_citation_verifier_tool_returns_valid_unsupported_result_without_citations() -> None:
    result = citation_verifier_tool(
        "Coverage applies for emergencies.",
        [],
        [make_chunk()],
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.verification.supported is False
    assert result.result.verification.confidence == "low"
    assert result.result.verification.missing_citations


def test_citation_verifier_tool_returns_valid_weak_support_result() -> None:
    result = citation_verifier_tool(
        "Premium discounts apply to annual renewals.",
        [make_citation()],
        [make_chunk()],
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.verification.supported is False
    assert result.result.verification.confidence == "medium"
    assert result.result.notes


def test_citation_verifier_tool_returns_valid_partial_support_result() -> None:
    matched_citation = make_citation()
    unmatched_citation = make_citation(
        document_name="Policy B",
        chunk_id="policy-b:v2:0003",
        page=8,
        section="Exclusions",
        clause_id="3.4",
    )

    result = citation_verifier_tool(
        "Hospitalization coverage applies for listed emergencies.",
        [matched_citation, unmatched_citation],
        [make_chunk()],
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.verification.supported is False
    assert result.result.reviewed_citations == [matched_citation]
    assert result.result.notes
    assert result.result.verification.missing_citations


def test_citation_verifier_output_remains_traceable_to_cited_evidence() -> None:
    citation = make_citation()
    result = citation_verifier_tool(
        "Hospitalization coverage applies for listed emergencies.",
        [citation],
        [make_chunk()],
    )

    assert result.result is not None
    assert result.result.reviewed_citations == [citation]


def test_citation_verifier_tool_returns_typed_input_validation_failure() -> None:
    result = citation_verifier_tool(
        "",
        [make_citation()],
        [make_chunk()],
    )

    assert result.ok is False
    assert result.error is not None
    assert result.error.kind == "input_validation_failure"


def test_citation_verifier_tool_failure_remains_observable(caplog) -> None:
    caplog.set_level(logging.INFO)

    original = verifier_module.verify_citations_against_evidence

    def explode(*_args, **_kwargs):
        raise RuntimeError("verify failed")

    verifier_module.verify_citations_against_evidence = explode
    try:
        result = citation_verifier_tool(
            "Hospitalization coverage applies for listed emergencies.",
            [make_citation()],
            [make_chunk()],
            request_id="verify-123456789012",
        )
    finally:
        verifier_module.verify_citations_against_evidence = original

    assert result.ok is False
    assert result.error is not None
    assert result.error.kind == "verification_failure"
    assert any(
        getattr(record, "event_type", "") == "citation_verifier_tool_started"
        for record in caplog.records
    )
    failed = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", "") == "citation_verifier_tool_failed"
    )
    assert failed.request_id == "verify-123456789012"


def test_citation_verifier_tool_success_preserves_request_correlation(caplog) -> None:
    caplog.set_level(logging.INFO)

    result = citation_verifier_tool(
        "Hospitalization coverage applies for listed emergencies.",
        [make_citation()],
        [make_chunk()],
        request_id="verify-123456789012",
    )

    assert result.ok is True
    succeeded = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", "") == "citation_verifier_tool_succeeded"
    )
    assert succeeded.request_id == "verify-123456789012"
    assert succeeded.duration_ms >= 0


def test_classify_citation_verifier_error_distinguishes_runtime_failure() -> None:
    error = classify_citation_verifier_error(RuntimeError("verify failed"))

    assert error.kind == "verification_failure"
