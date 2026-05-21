"""Hosted-like latency-budget validation for product-facing query classification."""

from __future__ import annotations

import time
from collections.abc import Callable

from contracts import (
    QueryClassificationHostedLatencyBudgetValidationResult,
    QueryClassificationOptimizationInput,
    QueryClassificationOptimizationOutput,
)
from core.dspy_query_classification import create_optimized_query_classification_predictor
from core.optimization_dataset import load_query_classification_optimization_dataset
from core.query_classification_latency import run_query_classification_latency_comparison

DEFAULT_HOSTED_QUERY_CLASSIFICATION_LATENCY_BUDGET_MS = 5.0
PRODUCT_FACING_QUERY_CLASSIFICATION_SURFACE = "product_facing_query_classification"


def execute_product_facing_query_classification(
    user_query: str,
    *,
    optimized_classifier: Callable[
        [QueryClassificationOptimizationInput], QueryClassificationOptimizationOutput
    ],
) -> QueryClassificationOptimizationOutput:
    """Execute the narrow product-facing classification request path."""

    normalized_query = user_query.strip()
    optimization_input = QueryClassificationOptimizationInput(user_query=normalized_query)
    return optimized_classifier(optimization_input)



def run_hosted_query_classification_latency_budget_validation(
    *,
    latency_budget_ms: float = DEFAULT_HOSTED_QUERY_CLASSIFICATION_LATENCY_BUDGET_MS,
    optimized_classifier: Callable[
        [QueryClassificationOptimizationInput], QueryClassificationOptimizationOutput
    ]
    | None = None,
    comparison_timer: Callable[[], float] | None = None,
    request_timer: Callable[[], float] | None = None,
) -> QueryClassificationHostedLatencyBudgetValidationResult:
    """Validate hosted-like latency on the product-facing classification path."""

    resolved_optimized_classifier = (
        optimized_classifier or create_optimized_query_classification_predictor()
    )
    comparison_result = run_query_classification_latency_comparison(
        optimized_classifier=resolved_optimized_classifier,
        timer=comparison_timer,
    )

    dataset = load_query_classification_optimization_dataset()
    request_timer_fn = request_timer or time.perf_counter
    hosted_total_latency_ms = 0.0

    for example in dataset.examples:
        started_at = request_timer_fn()
        execute_product_facing_query_classification(
            example.user_query,
            optimized_classifier=resolved_optimized_classifier,
        )
        hosted_total_latency_ms += round((request_timer_fn() - started_at) * 1000, 6)

    hosted_average_latency_ms = round(hosted_total_latency_ms / len(dataset.examples), 6)
    within_budget = hosted_average_latency_ms <= latency_budget_ms
    budget_state = "within_budget" if within_budget else "over_budget"

    return QueryClassificationHostedLatencyBudgetValidationResult(
        dataset_version=dataset.version,
        example_count=len(dataset.examples),
        request_surface=PRODUCT_FACING_QUERY_CLASSIFICATION_SURFACE,
        latency_budget_ms=latency_budget_ms,
        comparison_average_latency_ms=comparison_result.optimized_average_latency_ms,
        hosted_average_latency_ms=hosted_average_latency_ms,
        budget_state=budget_state,
        within_budget=within_budget,
    )
