from __future__ import annotations

from collections import deque

from contracts import QueryClassificationLatencyBudgetValidationResult
from core.query_classification_latency_budget import (
    DEFAULT_QUERY_CLASSIFICATION_LATENCY_BUDGET_MS,
    run_query_classification_latency_budget_validation,
)


def test_run_query_classification_latency_budget_validation_returns_typed_result() -> None:
    result = run_query_classification_latency_budget_validation()

    assert isinstance(result, QueryClassificationLatencyBudgetValidationResult)
    assert result.dataset_version == "2026-05-20-query-classification-subset-v1"
    assert result.example_count == 10


def test_run_query_classification_latency_budget_validation_reports_within_budget() -> None:
    timeline = deque(
        [
            0.0,
            0.001,
            0.001,
            0.003,
        ]
        * 10
    )

    result = run_query_classification_latency_budget_validation(
        timer=lambda: timeline.popleft(),
        latency_budget_ms=DEFAULT_QUERY_CLASSIFICATION_LATENCY_BUDGET_MS,
    )

    assert result.baseline_average_latency_ms == 1.0
    assert result.optimized_average_latency_ms == 2.0
    assert result.latency_budget_ms == DEFAULT_QUERY_CLASSIFICATION_LATENCY_BUDGET_MS
    assert result.within_budget is True
    assert result.budget_state == "within_budget"


def test_run_query_classification_latency_budget_validation_reports_over_budget() -> None:
    timeline = deque(
        [
            0.0,
            0.001,
            0.001,
            0.007,
        ]
        * 10
    )

    result = run_query_classification_latency_budget_validation(
        timer=lambda: timeline.popleft(),
        latency_budget_ms=5.0,
    )

    assert result.optimized_average_latency_ms == 6.0
    assert result.within_budget is False
    assert result.budget_state == "over_budget"
