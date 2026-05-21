"""Cost comparison helpers for query-classification optimization."""

from __future__ import annotations

from collections.abc import Callable

from contracts import (
    QueryClassificationCostComparisonResult,
    QueryClassificationExampleCostResult,
    QueryClassificationOptimizationInput,
)
from core.optimization_dataset import load_query_classification_optimization_dataset

CostEstimate = tuple[int, float]


def run_query_classification_cost_comparison(
    *,
    optimized_cost_evaluator: Callable[[QueryClassificationOptimizationInput], CostEstimate]
    | None = None,
) -> QueryClassificationCostComparisonResult:
    """Compare baseline versus optimized cost for query classification."""

    dataset = load_query_classification_optimization_dataset()
    cost_evaluator = optimized_cost_evaluator or (lambda _optimization_input: (0, 0.0))

    example_results: list[QueryClassificationExampleCostResult] = []
    optimized_total_external_call_count = 0
    optimized_total_estimated_cost_units = 0.0

    for example in dataset.examples:
        optimization_input = QueryClassificationOptimizationInput(user_query=example.user_query)
        optimized_external_call_count, optimized_estimated_cost_units = cost_evaluator(
            optimization_input
        )

        optimized_total_external_call_count += optimized_external_call_count
        optimized_total_estimated_cost_units += optimized_estimated_cost_units
        example_results.append(
            QueryClassificationExampleCostResult(
                example_id=example.example_id,
                source_question_id=example.source_question_id,
                baseline_external_call_count=0,
                optimized_external_call_count=optimized_external_call_count,
                baseline_estimated_cost_units=0.0,
                optimized_estimated_cost_units=optimized_estimated_cost_units,
            )
        )

    example_count = len(example_results)
    return QueryClassificationCostComparisonResult(
        dataset_version=dataset.version,
        example_count=example_count,
        baseline_total_external_call_count=0,
        optimized_total_external_call_count=optimized_total_external_call_count,
        baseline_total_estimated_cost_units=0.0,
        optimized_total_estimated_cost_units=round(optimized_total_estimated_cost_units, 6),
        baseline_average_estimated_cost_units=0.0,
        optimized_average_estimated_cost_units=round(
            optimized_total_estimated_cost_units / example_count,
            6,
        ),
        example_results=example_results,
    )
