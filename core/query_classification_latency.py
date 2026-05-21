"""Latency comparison helpers for query-classification optimization."""

from __future__ import annotations

import time
from collections.abc import Callable

from contracts import (
    QueryClassificationExampleLatencyResult,
    QueryClassificationLatencyComparisonResult,
    QueryClassificationOptimizationInput,
    QueryClassificationOptimizationOutput,
)
from core.optimization_dataset import load_query_classification_optimization_dataset
from core.query_classification_quality import classify_optimization_example_with_baseline


def run_query_classification_latency_comparison(
    *,
    optimized_classifier: Callable[
        [QueryClassificationOptimizationInput], QueryClassificationOptimizationOutput
    ]
    | None = None,
    timer: Callable[[], float] | None = None,
) -> QueryClassificationLatencyComparisonResult:
    """Compare baseline versus optimized latency for query classification."""

    dataset = load_query_classification_optimization_dataset()
    timer_fn = timer or time.perf_counter

    example_results: list[QueryClassificationExampleLatencyResult] = []
    baseline_total_latency_ms = 0.0
    optimized_total_latency_ms = 0.0

    for example in dataset.examples:
        optimization_input = QueryClassificationOptimizationInput(user_query=example.user_query)

        baseline_started_at = timer_fn()
        classify_optimization_example_with_baseline(example)
        baseline_latency_ms = round((timer_fn() - baseline_started_at) * 1000, 6)

        optimized_started_at = timer_fn()
        if optimized_classifier is None:
            classify_optimization_example_with_baseline(example)
        else:
            optimized_classifier(optimization_input)
        optimized_latency_ms = round((timer_fn() - optimized_started_at) * 1000, 6)

        baseline_total_latency_ms += baseline_latency_ms
        optimized_total_latency_ms += optimized_latency_ms
        example_results.append(
            QueryClassificationExampleLatencyResult(
                example_id=example.example_id,
                source_question_id=example.source_question_id,
                baseline_latency_ms=baseline_latency_ms,
                optimized_latency_ms=optimized_latency_ms,
            )
        )

    example_count = len(example_results)
    return QueryClassificationLatencyComparisonResult(
        dataset_version=dataset.version,
        example_count=example_count,
        baseline_total_latency_ms=round(baseline_total_latency_ms, 6),
        optimized_total_latency_ms=round(optimized_total_latency_ms, 6),
        baseline_average_latency_ms=round(baseline_total_latency_ms / example_count, 6),
        optimized_average_latency_ms=round(optimized_total_latency_ms / example_count, 6),
        example_results=example_results,
    )
