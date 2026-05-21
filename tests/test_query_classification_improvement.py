from __future__ import annotations

from contracts import QueryClassificationQualityImprovementValidationResult
from core.query_classification_improvement import (
    run_query_classification_quality_improvement_validation,
)


def test_run_query_classification_quality_improvement_validation_returns_typed_result() -> None:
    result = run_query_classification_quality_improvement_validation()

    assert isinstance(result, QueryClassificationQualityImprovementValidationResult)
    assert result.dataset_version == "2026-05-20-query-classification-subset-v1"
    assert result.evaluation_surface == "query_classification_optimization_subset"


def test_run_query_classification_quality_improvement_validation_reports_state() -> None:
    result = run_query_classification_quality_improvement_validation()

    assert result.improvement_state in {"improved", "flat", "regressed"}
    assert round(result.optimized_accuracy - result.baseline_accuracy, 6) == result.accuracy_delta


def test_run_query_classification_quality_improvement_validation_is_currently_flat() -> None:
    result = run_query_classification_quality_improvement_validation()

    assert result.baseline_accuracy == 1.0
    assert result.optimized_accuracy == 1.0
    assert result.improvement_state == "flat"
    assert result.measurable_improvement_validated is False
    assert result.accuracy_delta == 0.0
    assert "No measurable improvement is currently validated" in result.conclusion
