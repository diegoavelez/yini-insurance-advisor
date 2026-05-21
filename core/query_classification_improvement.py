"""Quality-improvement validation helpers for query-classification optimization."""

from __future__ import annotations

from contracts import QueryClassificationQualityImprovementValidationResult
from core.dspy_query_classification import create_optimized_query_classification_predictor
from core.query_classification_quality import run_query_classification_quality_comparison


def run_query_classification_quality_improvement_validation() -> (
    QueryClassificationQualityImprovementValidationResult
):
    """Validate whether the optimized predictor improves over the baseline."""

    optimized_predictor = create_optimized_query_classification_predictor()
    comparison_result = run_query_classification_quality_comparison(
        optimized_classifier=optimized_predictor
    )
    accuracy_delta = round(
        comparison_result.optimized_accuracy - comparison_result.baseline_accuracy,
        6,
    )
    if accuracy_delta > 0:
        improvement_state = "improved"
    elif accuracy_delta < 0:
        improvement_state = "regressed"
    else:
        improvement_state = "flat"

    return QueryClassificationQualityImprovementValidationResult(
        dataset_version=comparison_result.dataset_version,
        baseline_accuracy=comparison_result.baseline_accuracy,
        optimized_accuracy=comparison_result.optimized_accuracy,
        improvement_state=improvement_state,
        accuracy_delta=accuracy_delta,
    )
