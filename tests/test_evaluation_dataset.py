from __future__ import annotations

from pathlib import Path

import pytest

from contracts import EvaluationQuestionSet
from core.evaluation_dataset import load_evaluation_question_set


def test_load_evaluation_question_set_returns_typed_dataset() -> None:
    question_set = load_evaluation_question_set()

    assert isinstance(question_set, EvaluationQuestionSet)
    assert question_set.version == "2026-05-19-target-30-complete"
    assert len(question_set.questions) == 30


def test_evaluation_question_set_covers_required_categories() -> None:
    question_set = load_evaluation_question_set()

    categories = {question.category for question in question_set.questions}
    assert "grounded_qa" in categories
    assert "unsupported_query" in categories
    assert "prompt_injection" in categories
    assert "citation_guardrail" in categories
    assert "confidence_guardrail" in categories


def test_evaluation_question_set_balances_current_categories() -> None:
    question_set = load_evaluation_question_set()

    category_counts: dict[str, int] = {}
    for question in question_set.questions:
        category_counts[question.category] = category_counts.get(question.category, 0) + 1

    assert category_counts == {
        "grounded_qa": 6,
        "unsupported_query": 6,
        "prompt_injection": 6,
        "citation_guardrail": 6,
        "confidence_guardrail": 6,
    }


def test_evaluation_question_ids_are_unique() -> None:
    question_set = load_evaluation_question_set()

    question_ids = [question.question_id for question in question_set.questions]
    assert len(question_ids) == len(set(question_ids))


def test_invalid_question_set_with_duplicate_ids_fails_validation(tmp_path: Path) -> None:
    invalid_dataset_path = tmp_path / "invalid-questions.json"
    invalid_dataset_path.write_text(
        """
{
  "version": "invalid",
  "questions": [
    {
      "question_id": "dup-001",
      "prompt": "First prompt",
      "category": "grounded_qa",
      "expected_behavior": "normal_answer",
      "rationale": "First."
    },
    {
      "question_id": "dup-001",
      "prompt": "Second prompt",
      "category": "unsupported_query",
      "expected_behavior": "scope_refusal",
      "rationale": "Second."
    }
  ]
}
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unique"):
        load_evaluation_question_set(invalid_dataset_path)
