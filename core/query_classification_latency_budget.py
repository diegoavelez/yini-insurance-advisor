"""Latency-budget validation helpers for query-classification optimization."""

from __future__ import annotations

from collections.abc import Callable

from contracts import (
    QueryClassificationLatencyBudgetValidationResult,
    QueryClassificationOptimizationInput,
    QueryClassificationOptimizationOutput,
)
from core.dspy_query_classification import create_optimized_query_classification_predictor
from core.query_classification_latency import run_query_classification_latency_comparison

DEFAULT_QUERY_CLASSIFICATION_LATENCY_BUDGET_MS = 5.0


def run_query_classification_latency_budget_validation(
    *,
    latency_budget_ms: float = DEFAULT_QUERY_CLASSIFICATION_LATENCY_BUDGET_MS,
    optimized_classifier: Callable[
        [QueryClassificationOptimizationInput], QueryClassificationOptimizationOutput
    ]
    | None = None,
    timer: Callable[[], float] | None = None,
) -> QueryClassificationLatencyBudgetValidationResult:
    """Validate whether the optimized path remains within the latency budget."""

    resolved_optimized_classifier = (
        optimized_classifier or create_optimized_query_classification_predictor()
    )
    comparison_result = run_query_classification_latency_comparison(
        optimized_classifier=resolved_optimized_classifier,
        timer=timer,
    )
    within_budget = comparison_result.optimized_average_latency_ms <= latency_budget_ms
    budget_state = "within_budget" if within_budget else "over_budget"

    return QueryClassificationLatencyBudgetValidationResult(
        dataset_version=comparison_result.dataset_version,
        example_count=comparison_result.example_count,
        latency_budget_ms=latency_budget_ms,
        baseline_average_latency_ms=comparison_result.baseline_average_latency_ms,
        optimized_average_latency_ms=comparison_result.optimized_average_latency_ms,
        budget_state=budget_state,
        within_budget=within_budget,
    )
