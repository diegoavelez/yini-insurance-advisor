"""Quality-improvement validation helpers for query-classification optimization."""

from __future__ import annotations

from contracts import QueryClassificationQualityImprovementValidationResult
from core.dspy_query_classification import create_optimized_query_classification_predictor
from core.query_classification_quality import run_query_classification_quality_comparison


def run_query_classification_quality_improvement_validation() -> (
    QueryClassificationQualityImprovementValidationResult
):
    """Report whether measurable improvement is actually validated today."""

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

    measurable_improvement_validated = improvement_state == "improved"
    if measurable_improvement_validated:
        conclusion = (
            "The optimized query-classification path demonstrates measurable "
            "improvement on the current optimization subset."
        )
    elif improvement_state == "flat":
        conclusion = (
            "No measurable improvement is currently validated on the query-"
            "classification optimization subset; the optimized path is "
            "functionally flat against the deterministic baseline."
        )
    else:
        conclusion = (
            "The optimized query-classification path currently regresses on "
            "the optimization subset and does not validate measurable "
            "improvement."
        )

    return QueryClassificationQualityImprovementValidationResult(
        dataset_version=comparison_result.dataset_version,
        evaluation_surface="query_classification_optimization_subset",
        baseline_accuracy=comparison_result.baseline_accuracy,
        optimized_accuracy=comparison_result.optimized_accuracy,
        improvement_state=improvement_state,
        measurable_improvement_validated=measurable_improvement_validated,
        accuracy_delta=accuracy_delta,
        conclusion=conclusion,
    )
