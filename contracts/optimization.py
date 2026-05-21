"""Optimization contracts for future DSPy-based work."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from contracts.evaluation import EvaluationQuestionCategory, ExpectedBehavior


class QueryClassificationOptimizationInput(BaseModel):
    """One typed optimization input for query classification."""

    user_query: str = Field(min_length=1)


class QueryClassificationOptimizationOutput(BaseModel):
    """One typed optimization output for query classification."""

    expected_behavior: ExpectedBehavior
    rationale: str = Field(min_length=1)


class QueryClassificationOptimizationExample(BaseModel):
    """One typed optimization example for query classification."""

    example_id: str = Field(min_length=1)
    source_question_id: str = Field(min_length=1)
    user_query: str = Field(min_length=1)
    category: EvaluationQuestionCategory
    expected_behavior: ExpectedBehavior
    rationale: str = Field(min_length=1)


class QueryClassificationOptimizationDataset(BaseModel):
    """Versioned typed optimization subset for query classification."""

    version: str = Field(min_length=1)
    examples: list[QueryClassificationOptimizationExample] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_ids(self) -> QueryClassificationOptimizationDataset:
        example_ids = [example.example_id for example in self.examples]
        if len(example_ids) != len(set(example_ids)):
            raise ValueError("optimization example ids must be unique.")

        source_question_ids = [example.source_question_id for example in self.examples]
        if len(source_question_ids) != len(set(source_question_ids)):
            raise ValueError("optimization source question ids must be unique.")
        return self


class QueryClassificationExampleQualityResult(BaseModel):
    """One baseline-versus-optimized quality result for one optimization example."""

    example_id: str = Field(min_length=1)
    source_question_id: str = Field(min_length=1)
    category: EvaluationQuestionCategory
    expected_behavior: ExpectedBehavior
    baseline_behavior: ExpectedBehavior
    optimized_behavior: ExpectedBehavior
    baseline_matched: bool
    optimized_matched: bool


class QueryClassificationCategoryQualityResult(BaseModel):
    """Aggregated quality result for one query-classification category."""

    category: EvaluationQuestionCategory
    example_count: int = Field(ge=1)
    baseline_matched_count: int = Field(ge=0)
    optimized_matched_count: int = Field(ge=0)
    baseline_accuracy: float = Field(ge=0.0, le=1.0)
    optimized_accuracy: float = Field(ge=0.0, le=1.0)


class QueryClassificationQualityComparisonResult(BaseModel):
    """Typed quality comparison result for query classification optimization."""

    dataset_version: str = Field(min_length=1)
    example_count: int = Field(ge=1)
    baseline_accuracy: float = Field(ge=0.0, le=1.0)
    optimized_accuracy: float = Field(ge=0.0, le=1.0)
    category_results: list[QueryClassificationCategoryQualityResult] = Field(min_length=1)
    example_results: list[QueryClassificationExampleQualityResult] = Field(min_length=1)


class QueryClassificationExampleLatencyResult(BaseModel):
    """One baseline-versus-optimized latency result for one optimization example."""

    example_id: str = Field(min_length=1)
    source_question_id: str = Field(min_length=1)
    baseline_latency_ms: float = Field(ge=0.0)
    optimized_latency_ms: float = Field(ge=0.0)


class QueryClassificationLatencyComparisonResult(BaseModel):
    """Typed latency comparison result for query classification optimization."""

    dataset_version: str = Field(min_length=1)
    example_count: int = Field(ge=1)
    baseline_total_latency_ms: float = Field(ge=0.0)
    optimized_total_latency_ms: float = Field(ge=0.0)
    baseline_average_latency_ms: float = Field(ge=0.0)
    optimized_average_latency_ms: float = Field(ge=0.0)
    example_results: list[QueryClassificationExampleLatencyResult] = Field(min_length=1)


class QueryClassificationExampleCostResult(BaseModel):
    """One baseline-versus-optimized cost result for one optimization example."""

    example_id: str = Field(min_length=1)
    source_question_id: str = Field(min_length=1)
    baseline_external_call_count: int = Field(ge=0)
    optimized_external_call_count: int = Field(ge=0)
    baseline_estimated_cost_units: float = Field(ge=0.0)
    optimized_estimated_cost_units: float = Field(ge=0.0)


class QueryClassificationCostComparisonResult(BaseModel):
    """Typed cost comparison result for query classification optimization."""

    dataset_version: str = Field(min_length=1)
    example_count: int = Field(ge=1)
    baseline_total_external_call_count: int = Field(ge=0)
    optimized_total_external_call_count: int = Field(ge=0)
    baseline_total_estimated_cost_units: float = Field(ge=0.0)
    optimized_total_estimated_cost_units: float = Field(ge=0.0)
    baseline_average_estimated_cost_units: float = Field(ge=0.0)
    optimized_average_estimated_cost_units: float = Field(ge=0.0)
    example_results: list[QueryClassificationExampleCostResult] = Field(min_length=1)


QueryClassificationImprovementState = Literal["improved", "flat", "regressed"]


class QueryClassificationQualityImprovementValidationResult(BaseModel):
    """Typed validation result for query-classification quality improvement."""

    dataset_version: str = Field(min_length=1)
    baseline_accuracy: float = Field(ge=0.0, le=1.0)
    optimized_accuracy: float = Field(ge=0.0, le=1.0)
    improvement_state: QueryClassificationImprovementState
    accuracy_delta: float
