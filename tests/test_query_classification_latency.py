from __future__ import annotations

from collections import deque

from contracts import (
    QueryClassificationLatencyComparisonResult,
    QueryClassificationOptimizationInput,
    QueryClassificationOptimizationOutput,
)
from core.query_classification_latency import run_query_classification_latency_comparison


def test_run_query_classification_latency_comparison_returns_typed_result() -> None:
    result = run_query_classification_latency_comparison()

    assert isinstance(result, QueryClassificationLatencyComparisonResult)
    assert result.dataset_version == "2026-06-08-query-classification-subset-spanish-v1"
    assert result.example_count == 10
    assert len(result.example_results) == 10


def test_run_query_classification_latency_comparison_reports_explicit_totals() -> None:
    timeline = deque(
        [
            0.0,
            0.001,
            0.001,
            0.003,
        ]
        * 10
    )

    result = run_query_classification_latency_comparison(
        timer=lambda: timeline.popleft()
    )

    assert result.baseline_total_latency_ms == 10.0
    assert result.optimized_total_latency_ms == 20.0
    assert result.baseline_average_latency_ms == 1.0
    assert result.optimized_average_latency_ms == 2.0


def test_run_query_classification_latency_comparison_uses_default_baseline_for_optimized() -> None:
    result = run_query_classification_latency_comparison()

    assert result.baseline_total_latency_ms >= 0.0
    assert result.optimized_total_latency_ms >= 0.0


def test_run_query_classification_latency_comparison_detects_slower_optimized_path() -> None:
    timeline = deque(
        [
            0.0,
            0.001,
            0.001,
            0.004,
        ]
        * 10
    )

    def optimized_classifier(
        optimization_input: QueryClassificationOptimizationInput,
    ) -> QueryClassificationOptimizationOutput:
        return QueryClassificationOptimizationOutput(
            expected_behavior="normal_answer",
            rationale=f"Timed optimized path for {optimization_input.user_query}",
        )

    result = run_query_classification_latency_comparison(
        optimized_classifier=optimized_classifier,
        timer=lambda: timeline.popleft(),
    )

    assert result.optimized_total_latency_ms > result.baseline_total_latency_ms
    assert result.optimized_average_latency_ms > result.baseline_average_latency_ms
