"""Evaluation dataset contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

EvaluationQuestionCategory = Literal[
    "grounded_qa",
    "unsupported_query",
    "prompt_injection",
    "citation_guardrail",
    "confidence_guardrail",
]

ExpectedBehavior = Literal[
    "normal_answer",
    "scope_refusal",
    "prompt_injection_refusal",
    "citation_guardrail",
    "confidence_guardrail",
]

RetrievalExpectationKind = Literal[
    "grounded_retrieval_required",
    "no_retrieval_expected",
    "guardrail_retrieval_expected",
]

CitationExpectationKind = Literal[
    "citations_required",
    "no_citations_expected",
    "guardrail_citation_posture",
]

EvaluationResultStatus = Literal["matched", "mismatched", "skipped"]


class EvaluationQuestion(BaseModel):
    """One typed evaluation question entry."""

    question_id: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    category: EvaluationQuestionCategory
    expected_behavior: ExpectedBehavior
    rationale: str = Field(min_length=1)


class EvaluationQuestionSet(BaseModel):
    """Versioned typed set of evaluation questions."""

    version: str = Field(min_length=1)
    questions: list[EvaluationQuestion] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_question_ids(self) -> EvaluationQuestionSet:
        question_ids = [question.question_id for question in self.questions]
        if len(question_ids) != len(set(question_ids)):
            raise ValueError("evaluation question ids must be unique.")
        return self


class GoldenBehaviorExpectation(BaseModel):
    """One explicit expected behavior entry linked to a question id."""

    question_id: str = Field(min_length=1)
    expected_behavior: ExpectedBehavior


class GoldenBehaviorSet(BaseModel):
    """Versioned golden behavior expectations for the evaluation question set."""

    version: str = Field(min_length=1)
    expectations: list[GoldenBehaviorExpectation] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_question_ids(self) -> GoldenBehaviorSet:
        question_ids = [expectation.question_id for expectation in self.expectations]
        if len(question_ids) != len(set(question_ids)):
            raise ValueError("golden behavior question ids must be unique.")
        return self


class RetrievalExpectationAnnotation(BaseModel):
    """One explicit retrieval expectation entry linked to a question id."""

    question_id: str = Field(min_length=1)
    retrieval_expectation: RetrievalExpectationKind


class RetrievalExpectationSet(BaseModel):
    """Versioned retrieval expectations for the evaluation question set."""

    version: str = Field(min_length=1)
    expectations: list[RetrievalExpectationAnnotation] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_question_ids(self) -> RetrievalExpectationSet:
        question_ids = [expectation.question_id for expectation in self.expectations]
        if len(question_ids) != len(set(question_ids)):
            raise ValueError("retrieval expectation question ids must be unique.")
        return self


class CitationExpectationAnnotation(BaseModel):
    """One explicit citation expectation entry linked to a question id."""

    question_id: str = Field(min_length=1)
    citation_expectation: CitationExpectationKind


class CitationExpectationSet(BaseModel):
    """Versioned citation expectations for the evaluation question set."""

    version: str = Field(min_length=1)
    expectations: list[CitationExpectationAnnotation] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_question_ids(self) -> CitationExpectationSet:
        question_ids = [expectation.question_id for expectation in self.expectations]
        if len(question_ids) != len(set(question_ids)):
            raise ValueError("citation expectation question ids must be unique.")
        return self


class EvaluationQuestionResult(BaseModel):
    """Typed result for one evaluated question."""

    question_id: str = Field(min_length=1)
    status: EvaluationResultStatus
    actual_behavior: ExpectedBehavior | None = None
    expected_behavior: ExpectedBehavior
    notes: str | None = None


class EvaluationRunResult(BaseModel):
    """Typed result for one local evaluation run."""

    run_id: str = Field(min_length=1)
    question_set_version: str = Field(min_length=1)
    golden_behavior_version: str = Field(min_length=1)
    results: list[EvaluationQuestionResult] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_question_ids(self) -> EvaluationRunResult:
        question_ids = [result.question_id for result in self.results]
        if len(question_ids) != len(set(question_ids)):
            raise ValueError("evaluation run result question ids must be unique.")
        return self
