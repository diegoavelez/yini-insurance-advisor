"""Local evaluation dataset loading helpers."""

from __future__ import annotations

import json
from pathlib import Path

from contracts.evaluation import EvaluationQuestionSet, GoldenBehaviorSet

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EVALUATION_QUESTION_SET_PATH = PROJECT_ROOT / "data" / "eval" / "questions.json"
DEFAULT_GOLDEN_BEHAVIOR_SET_PATH = PROJECT_ROOT / "data" / "eval" / "golden-behaviors.json"


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
