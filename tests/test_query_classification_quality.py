from __future__ import annotations

from contracts import (
    QueryClassificationOptimizationInput,
    QueryClassificationOptimizationOutput,
    QueryClassificationQualityComparisonResult,
)
from core.query_classification_quality import run_query_classification_quality_comparison


def test_run_query_classification_quality_comparison_returns_typed_result() -> None:
    result = run_query_classification_quality_comparison()

    assert isinstance(result, QueryClassificationQualityComparisonResult)
    assert result.dataset_version == "2026-05-20-query-classification-subset-v1"
    assert result.example_count == 10
    assert len(result.category_results) == 5
    assert len(result.example_results) == 10


def test_run_query_classification_quality_comparison_reports_per_category_quality() -> None:
    result = run_query_classification_quality_comparison()

    category_results = {
        category_result.category: category_result
        for category_result in result.category_results
    }
    assert set(category_results) == {
        "grounded_qa",
        "unsupported_query",
        "prompt_injection",
        "citation_guardrail",
        "confidence_guardrail",
    }
    assert all(category_result.example_count == 2 for category_result in category_results.values())


def test_run_query_classification_quality_comparison_uses_same_baseline_by_default() -> None:
    result = run_query_classification_quality_comparison()

    assert result.baseline_accuracy == 1.0
    assert result.optimized_accuracy == 1.0
    assert all(example_result.baseline_matched for example_result in result.example_results)
    assert all(example_result.optimized_matched for example_result in result.example_results)


def test_run_query_classification_quality_comparison_detects_optimized_regression() -> None:
    def regressing_classifier(
        optimization_input: QueryClassificationOptimizationInput,
    ) -> QueryClassificationOptimizationOutput:
        return QueryClassificationOptimizationOutput(
            expected_behavior="scope_refusal",
            rationale=f"Forced regression for: {optimization_input.user_query}",
        )

    result = run_query_classification_quality_comparison(
        optimized_classifier=regressing_classifier
    )

    assert result.baseline_accuracy == 1.0
    assert result.optimized_accuracy < result.baseline_accuracy
    category_results = {
        category_result.category: category_result
        for category_result in result.category_results
    }
    assert category_results["unsupported_query"].optimized_accuracy == 1.0
    assert category_results["grounded_qa"].optimized_accuracy == 0.0
