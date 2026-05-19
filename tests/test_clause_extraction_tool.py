from __future__ import annotations

import importlib
import logging

import pytest

from agents.clause_extraction_tool import (
    categorize_clause,
    classify_clause_tool_error,
    clause_extraction_tool,
)
from contracts import RetrievedChunk

clause_tool_module = importlib.import_module("agents.clause_extraction_tool")


def make_chunk(
    *,
    chunk_id: str = "chunk-v2-0",
    text: str = "Coverage applies after the waiting period.",
    document_name: str = "Policy A",
    clause_id: str | None = "COV-1",
) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=chunk_id,
        source_pdf_id="policy-1",
        chunk_schema_version="v2",
        chunk_index=0,
        text=text,
        document_name=document_name,
        document_version="2026",
        page=3,
        section="Coverage",
        section_path=["Coverage"],
        clause_id=clause_id,
        score=0.92,
    )


def test_clause_extraction_tool_returns_typed_success() -> None:
    tool_result = clause_extraction_tool(
        [make_chunk(text="Coverage applies after the waiting period.")],
    )

    assert tool_result.ok is True
    assert tool_result.error is None
    assert tool_result.result is not None
    assert len(tool_result.result.clauses) == 1
    assert tool_result.result.clauses[0].category == "coverage"


def test_clause_extraction_tool_treats_empty_extraction_as_success() -> None:
    tool_result = clause_extraction_tool(
        [make_chunk(text="This paragraph is informational and descriptive only.")],
    )

    assert tool_result.ok is True
    assert tool_result.result is not None
    assert tool_result.result.clauses == []
    assert tool_result.error is None


def test_clause_extraction_tool_preserves_supporting_chunk_traceability() -> None:
    tool_result = clause_extraction_tool(
        [make_chunk(chunk_id="chunk-v2-7", text="Coverage applies after the waiting period.")],
    )

    assert tool_result.result is not None
    assert tool_result.result.clauses[0].supporting_chunk_ids == ["chunk-v2-7"]
    assert tool_result.result.clauses[0].category in {
        "coverage",
        "exclusion",
        "restriction",
        "requirement",
        "procedure",
        "exception",
    }


def test_clause_extraction_tool_returns_typed_input_validation_failure() -> None:
    tool_result = clause_extraction_tool(["not-a-chunk"])  # type: ignore[list-item]

    assert tool_result.ok is False
    assert tool_result.result is None
    assert tool_result.error is not None
    assert tool_result.error.kind == "input_validation_failure"


def test_clause_extraction_tool_failure_remains_observable(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)
    monkeypatch.setattr(
        clause_tool_module,
        "extract_clause_from_chunk",
        lambda _chunk: (_ for _ in ()).throw(RuntimeError("extract failed")),
    )

    tool_result = clause_extraction_tool(
        [make_chunk()],
        request_id="tool-123456789012",
    )

    assert tool_result.ok is False
    assert tool_result.error is not None
    event_types = [record.event_type for record in caplog.records if hasattr(record, "event_type")]
    assert "clause_extraction_tool_started" in event_types
    assert "clause_extraction_tool_failed" in event_types
    failure_record = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "clause_extraction_tool_failed"
    )
    assert failure_record.request_id == "tool-123456789012"
    assert failure_record.error_message == "extract failed"


def test_clause_extraction_tool_success_preserves_request_correlation(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)

    tool_result = clause_extraction_tool(
        [make_chunk()],
        request_id="tool-123456789012",
    )

    assert tool_result.ok is True
    success_record = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "clause_extraction_tool_succeeded"
    )
    assert success_record.request_id == "tool-123456789012"
    assert success_record.duration_ms >= 0


@pytest.mark.parametrize(
    ("text", "expected_category"),
    [
        ("Coverage applies after the waiting period.", "coverage"),
        ("This exclusion applies to cosmetic procedures.", "exclusion"),
        ("The insured must submit the form within 30 days.", "requirement"),
        ("Follow this procedure to report a claim.", "procedure"),
        ("Coverage is subject to the listed restrictions.", "restriction"),
        ("The exception applies unless fraud is detected.", "exception"),
    ],
)
def test_categorize_clause_uses_existing_categories(text: str, expected_category: str) -> None:
    assert categorize_clause(text) == expected_category


def test_classify_clause_tool_error_distinguishes_runtime_failure() -> None:
    tool_error = classify_clause_tool_error(RuntimeError("extract failed"))

    assert tool_error.kind == "extraction_failure"
    assert tool_error.message == "extract failed"
