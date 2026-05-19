from __future__ import annotations

import importlib
import logging

import pytest

from agents.policy_comparison_tool import (
    classify_policy_comparison_error,
    policy_comparison_tool,
)
from contracts import Clause

policy_tool_module = importlib.import_module("agents.policy_comparison_tool")


def make_clause(
    *,
    category: str = "coverage",
    summary: str = "Coverage applies after the waiting period.",
    document_name: str = "Policy A",
    clause_id: str | None = "COV-1",
    supporting_chunk_ids: list[str] | None = None,
) -> Clause:
    return Clause(
        category=category,
        summary=summary,
        document_name=document_name,
        page=3,
        section="Coverage",
        clause_id=clause_id,
        supporting_chunk_ids=supporting_chunk_ids or ["chunk-v2-0"],
    )


def test_policy_comparison_tool_returns_structured_success() -> None:
    tool_result = policy_comparison_tool(
        [
            make_clause(document_name="Policy A"),
            make_clause(document_name="Policy B"),
        ]
    )

    assert tool_result.ok is True
    assert tool_result.error is None
    assert tool_result.result is not None
    assert len(tool_result.result.comparison_points) == 1
    assert tool_result.result.sufficient_information is True


def test_policy_comparison_tool_returns_valid_insufficient_information() -> None:
    tool_result = policy_comparison_tool([make_clause(document_name="Policy A")])

    assert tool_result.ok is True
    assert tool_result.result is not None
    assert tool_result.result.comparison_points == []
    assert tool_result.result.sufficient_information is False
    assert tool_result.result.notes != []


def test_policy_comparison_points_remain_traceable_to_source_documents() -> None:
    tool_result = policy_comparison_tool(
        [
            make_clause(document_name="Policy A"),
            make_clause(document_name="Policy B"),
        ]
    )

    assert tool_result.result is not None
    point = tool_result.result.comparison_points[0]
    assert point.source_documents == ["Policy A", "Policy B"]


def test_policy_comparison_tool_returns_typed_input_validation_failure() -> None:
    tool_result = policy_comparison_tool(["not-a-clause"])  # type: ignore[list-item]

    assert tool_result.ok is False
    assert tool_result.result is None
    assert tool_result.error is not None
    assert tool_result.error.kind == "input_validation_failure"


def test_policy_comparison_tool_failure_remains_observable(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)
    monkeypatch.setattr(
        policy_tool_module,
        "build_comparison_points",
        lambda _clauses: (_ for _ in ()).throw(RuntimeError("compare failed")),
    )

    tool_result = policy_comparison_tool(
        [make_clause()],
        request_id="tool-123456789012",
    )

    assert tool_result.ok is False
    assert tool_result.error is not None
    event_types = [record.event_type for record in caplog.records if hasattr(record, "event_type")]
    assert "policy_comparison_tool_started" in event_types
    assert "policy_comparison_tool_failed" in event_types
    failure_record = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "policy_comparison_tool_failed"
    )
    assert failure_record.request_id == "tool-123456789012"
    assert failure_record.error_message == "compare failed"


def test_policy_comparison_tool_success_preserves_request_correlation(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)

    tool_result = policy_comparison_tool(
        [
            make_clause(document_name="Policy A"),
            make_clause(document_name="Policy B"),
        ],
        request_id="tool-123456789012",
    )

    assert tool_result.ok is True
    success_record = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "policy_comparison_tool_succeeded"
    )
    assert success_record.request_id == "tool-123456789012"
    assert success_record.duration_ms >= 0


def test_classify_policy_comparison_error_distinguishes_runtime_failure() -> None:
    tool_error = classify_policy_comparison_error(RuntimeError("compare failed"))

    assert tool_error.kind == "comparison_failure"
    assert tool_error.message == "compare failed"
