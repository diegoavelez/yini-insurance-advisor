"""Local evaluation dataset loading helpers."""

from __future__ import annotations

import json
from pathlib import Path

from contracts.evaluation import (
    CitationExpectationSet,
    EvaluationQuestionSet,
    GoldenBehaviorSet,
    RetrievalExpectationSet,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EVALUATION_QUESTION_SET_PATH = PROJECT_ROOT / "data" / "eval" / "questions.json"
DEFAULT_GOLDEN_BEHAVIOR_SET_PATH = PROJECT_ROOT / "data" / "eval" / "golden-behaviors.json"
DEFAULT_RETRIEVAL_EXPECTATION_SET_PATH = (
    PROJECT_ROOT / "data" / "eval" / "retrieval-expectations.json"
)
DEFAULT_CITATION_EXPECTATION_SET_PATH = (
    PROJECT_ROOT / "data" / "eval" / "citation-expectations.json"
)


def load_evaluation_question_set(
    path: Path = DEFAULT_EVALUATION_QUESTION_SET_PATH,
) -> EvaluationQuestionSet:
    """Load and validate the local evaluation question set."""

    return EvaluationQuestionSet.model_validate_json(path.read_text(encoding="utf-8"))


def save_evaluation_question_set(
    question_set: EvaluationQuestionSet,
    path: Path = DEFAULT_EVALUATION_QUESTION_SET_PATH,
) -> None:
    """Persist the local evaluation question set in a stable JSON format."""

    path.write_text(
        json.dumps(question_set.model_dump(mode="json"), indent=2) + "\n",
        encoding="utf-8",
    )


def load_golden_behavior_set(
    path: Path = DEFAULT_GOLDEN_BEHAVIOR_SET_PATH,
) -> GoldenBehaviorSet:
    """Load and validate the local golden behavior expectation set."""

    return GoldenBehaviorSet.model_validate_json(path.read_text(encoding="utf-8"))


def validate_golden_behavior_alignment(
    question_set: EvaluationQuestionSet,
    golden_behavior_set: GoldenBehaviorSet,
) -> None:
    """Validate that golden behavior expectations map exactly to known questions."""

    question_ids = {question.question_id for question in question_set.questions}
    golden_question_ids = {
        expectation.question_id for expectation in golden_behavior_set.expectations
    }

    missing_question_ids = question_ids - golden_question_ids
    extra_question_ids = golden_question_ids - question_ids

    if extra_question_ids:
        raise ValueError("golden behavior set contains unknown question ids.")
    if missing_question_ids:
        raise ValueError("golden behavior set is missing question ids.")


def load_retrieval_expectation_set(
    path: Path = DEFAULT_RETRIEVAL_EXPECTATION_SET_PATH,
) -> RetrievalExpectationSet:
    """Load and validate the local retrieval expectation set."""

    return RetrievalExpectationSet.model_validate_json(path.read_text(encoding="utf-8"))


def validate_retrieval_expectation_alignment(
    question_set: EvaluationQuestionSet,
    retrieval_expectation_set: RetrievalExpectationSet,
) -> None:
    """Validate that retrieval expectations map exactly to known questions."""

    question_ids = {question.question_id for question in question_set.questions}
    retrieval_question_ids = {
        expectation.question_id for expectation in retrieval_expectation_set.expectations
    }

    missing_question_ids = question_ids - retrieval_question_ids
    extra_question_ids = retrieval_question_ids - question_ids

    if extra_question_ids:
        raise ValueError("retrieval expectation set contains unknown question ids.")
    if missing_question_ids:
        raise ValueError("retrieval expectation set is missing question ids.")


def load_citation_expectation_set(
    path: Path = DEFAULT_CITATION_EXPECTATION_SET_PATH,
) -> CitationExpectationSet:
    """Load and validate the local citation expectation set."""

    return CitationExpectationSet.model_validate_json(path.read_text(encoding="utf-8"))


def validate_citation_expectation_alignment(
    question_set: EvaluationQuestionSet,
    citation_expectation_set: CitationExpectationSet,
) -> None:
    """Validate that citation expectations map exactly to known questions."""

    question_ids = {question.question_id for question in question_set.questions}
    citation_question_ids = {
        expectation.question_id for expectation in citation_expectation_set.expectations
    }

    missing_question_ids = question_ids - citation_question_ids
    extra_question_ids = citation_question_ids - question_ids

    if extra_question_ids:
        raise ValueError("citation expectation set contains unknown question ids.")
    if missing_question_ids:
        raise ValueError("citation expectation set is missing question ids.")
