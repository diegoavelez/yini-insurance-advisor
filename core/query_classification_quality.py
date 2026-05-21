"""Quality comparison helpers for query-classification optimization."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from contracts import (
    EvaluationQuestionCategory,
    QueryClassificationCategoryQualityResult,
    QueryClassificationExampleQualityResult,
    QueryClassificationOptimizationExample,
    QueryClassificationOptimizationInput,
    QueryClassificationOptimizationOutput,
    QueryClassificationQualityComparisonResult,
)
from core.dspy_query_classification import classify_query_with_baseline
from core.optimization_dataset import load_query_classification_optimization_dataset


def run_query_classification_quality_comparison(
    *,
    optimized_classifier: Callable[
        [QueryClassificationOptimizationInput], QueryClassificationOptimizationOutput
    ]
    | None = None,
) -> QueryClassificationQualityComparisonResult:
    """Compare baseline versus optimized query-classification quality."""

    dataset = load_query_classification_optimization_dataset()
    example_results: list[QueryClassificationExampleQualityResult] = []
    for example in dataset.examples:
        optimization_input = QueryClassificationOptimizationInput(user_query=example.user_query)
        baseline_output = classify_optimization_example_with_baseline(example)
        if optimized_classifier is None:
            optimized_output = baseline_output
        else:
            optimized_output = optimized_classifier(optimization_input)
        example_results.append(
            QueryClassificationExampleQualityResult(
                example_id=example.example_id,
                source_question_id=example.source_question_id,
                category=example.category,
                expected_behavior=example.expected_behavior,
                baseline_behavior=baseline_output.expected_behavior,
                optimized_behavior=optimized_output.expected_behavior,
                baseline_matched=baseline_output.expected_behavior == example.expected_behavior,
                optimized_matched=optimized_output.expected_behavior == example.expected_behavior,
            )
        )

    category_results = build_category_quality_results(example_results)
    example_count = len(example_results)
    baseline_matched_count = sum(result.baseline_matched for result in example_results)
    optimized_matched_count = sum(result.optimized_matched for result in example_results)

    return QueryClassificationQualityComparisonResult(
        dataset_version=dataset.version,
        example_count=example_count,
        baseline_accuracy=baseline_matched_count / example_count,
        optimized_accuracy=optimized_matched_count / example_count,
        category_results=category_results,
        example_results=example_results,
    )


def build_category_quality_results(
    example_results: list[QueryClassificationExampleQualityResult],
) -> list[QueryClassificationCategoryQualityResult]:
    """Build per-category quality aggregates from per-example results."""

    grouped_results: dict[
        EvaluationQuestionCategory,
        list[QueryClassificationExampleQualityResult],
    ] = defaultdict(list)
    for result in example_results:
        grouped_results[result.category].append(result)

    category_results: list[QueryClassificationCategoryQualityResult] = []
    for category in sorted(grouped_results):
        grouped = grouped_results[category]
        example_count = len(grouped)
        baseline_matched_count = sum(result.baseline_matched for result in grouped)
        optimized_matched_count = sum(result.optimized_matched for result in grouped)
        category_results.append(
            QueryClassificationCategoryQualityResult(
                category=category,
                example_count=example_count,
                baseline_matched_count=baseline_matched_count,
                optimized_matched_count=optimized_matched_count,
                baseline_accuracy=baseline_matched_count / example_count,
                optimized_accuracy=optimized_matched_count / example_count,
            )
        )

    return category_results


def classify_optimization_example_with_baseline(
    example: QueryClassificationOptimizationExample,
) -> QueryClassificationOptimizationOutput:
    """Return the documented baseline classification for one optimization example."""

    optimization_input = QueryClassificationOptimizationInput(user_query=example.user_query)
    query_only_result = classify_query_with_baseline(optimization_input)
    if example.category == "prompt_injection":
        return QueryClassificationOptimizationOutput(
            expected_behavior="prompt_injection_refusal",
            rationale="Baseline evaluation treats prompt-injection examples as refusal cases.",
        )
    if example.category == "citation_guardrail":
        return QueryClassificationOptimizationOutput(
            expected_behavior="citation_guardrail",
            rationale="Baseline evaluation treats citation-guardrail examples as guarded cases.",
        )
    if example.category == "confidence_guardrail":
        return QueryClassificationOptimizationOutput(
            expected_behavior="confidence_guardrail",
            rationale="Baseline evaluation treats confidence-guardrail examples as guarded cases.",
        )
    return query_only_result
