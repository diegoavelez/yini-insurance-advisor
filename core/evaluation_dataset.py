"""Local evaluation dataset loading helpers."""

from __future__ import annotations

import json
from pathlib import Path

from contracts.evaluation import EvaluationQuestionSet

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EVALUATION_QUESTION_SET_PATH = PROJECT_ROOT / "data" / "eval" / "questions.json"


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
