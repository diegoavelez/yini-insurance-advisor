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
