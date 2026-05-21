"""Optimization contracts for future DSPy-based work."""

from __future__ import annotations

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
