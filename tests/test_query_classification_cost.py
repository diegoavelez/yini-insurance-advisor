from __future__ import annotations

from contracts import (
    QueryClassificationCostComparisonResult,
    QueryClassificationOptimizationInput,
)
from core.query_classification_cost import run_query_classification_cost_comparison


def test_run_query_classification_cost_comparison_returns_typed_result() -> None:
    result = run_query_classification_cost_comparison()

    assert isinstance(result, QueryClassificationCostComparisonResult)
    assert result.dataset_version == "2026-06-08-query-classification-subset-spanish-v1"
    assert result.example_count == 10
    assert len(result.example_results) == 10


def test_run_query_classification_cost_comparison_uses_zero_cost_baseline_by_default() -> None:
    result = run_query_classification_cost_comparison()

    assert result.baseline_total_external_call_count == 0
    assert result.optimized_total_external_call_count == 0
    assert result.baseline_total_estimated_cost_units == 0.0
    assert result.optimized_total_estimated_cost_units == 0.0


def test_run_query_classification_cost_comparison_reports_optimized_cost() -> None:
    def fixed_cost_evaluator(
        optimization_input: QueryClassificationOptimizationInput,
    ) -> tuple[int, float]:
        assert optimization_input.user_query
        return (1, 0.25)

    result = run_query_classification_cost_comparison(
        optimized_cost_evaluator=fixed_cost_evaluator
    )

    assert result.baseline_total_external_call_count == 0
    assert result.optimized_total_external_call_count == 10
    assert result.baseline_total_estimated_cost_units == 0.0
    assert result.optimized_total_estimated_cost_units == 2.5
    assert result.optimized_average_estimated_cost_units == 0.25
