from __future__ import annotations

from pathlib import Path

import pytest

from contracts import (
    CitationExpectationSet,
    EvaluationQuestionResult,
    EvaluationQuestionSet,
    EvaluationRunResult,
    GoldenBehaviorSet,
    RetrievalExpectationSet,
)
from core.evaluation_dataset import (
    load_citation_expectation_set,
    load_evaluation_question_set,
    load_golden_behavior_set,
    load_retrieval_expectation_set,
    validate_citation_expectation_alignment,
    validate_golden_behavior_alignment,
    validate_retrieval_expectation_alignment,
)


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


def test_load_golden_behavior_set_returns_typed_dataset() -> None:
    golden_behavior_set = load_golden_behavior_set()

    assert isinstance(golden_behavior_set, GoldenBehaviorSet)
    assert golden_behavior_set.version == "2026-05-19-golden-behaviors-v1"
    assert len(golden_behavior_set.expectations) == 30


def test_golden_behavior_set_covers_every_curated_question() -> None:
    question_set = load_evaluation_question_set()
    golden_behavior_set = load_golden_behavior_set()

    validate_golden_behavior_alignment(question_set, golden_behavior_set)


def test_grounded_questions_retain_normal_answer_expectations() -> None:
    golden_behavior_set = load_golden_behavior_set()

    expectations = {
        expectation.question_id: expectation.expected_behavior
        for expectation in golden_behavior_set.expectations
    }

    for question_id in ["qa-001", "qa-002", "qa-003", "qa-004", "qa-005", "qa-006"]:
        assert expectations[question_id] == "normal_answer"


def test_refusal_and_guardrail_questions_retain_explicit_expectations() -> None:
    golden_behavior_set = load_golden_behavior_set()

    expectations = {
        expectation.question_id: expectation.expected_behavior
        for expectation in golden_behavior_set.expectations
    }

    for question_id in ["scope-001", "scope-006"]:
        assert expectations[question_id] == "scope_refusal"
    for question_id in ["inj-001", "inj-006"]:
        assert expectations[question_id] == "prompt_injection_refusal"
    for question_id in ["cite-001", "cite-006"]:
        assert expectations[question_id] == "citation_guardrail"
    for question_id in ["conf-001", "conf-006"]:
        assert expectations[question_id] == "confidence_guardrail"


def test_invalid_golden_behavior_set_with_unknown_question_id_fails(tmp_path: Path) -> None:
    invalid_golden_behavior_path = tmp_path / "invalid-golden-behaviors.json"
    invalid_golden_behavior_path.write_text(
        """
{
  "version": "invalid",
  "expectations": [
    {
      "question_id": "unknown-001",
      "expected_behavior": "normal_answer"
    }
  ]
}
""".strip()
        + "\n",
        encoding="utf-8",
    )

    question_set = load_evaluation_question_set()
    golden_behavior_set = load_golden_behavior_set(invalid_golden_behavior_path)

    with pytest.raises(ValueError, match="unknown question ids"):
        validate_golden_behavior_alignment(question_set, golden_behavior_set)


def test_load_retrieval_expectation_set_returns_typed_dataset() -> None:
    retrieval_expectation_set = load_retrieval_expectation_set()

    assert isinstance(retrieval_expectation_set, RetrievalExpectationSet)
    assert retrieval_expectation_set.version == "2026-05-20-retrieval-expectations-v1"
    assert len(retrieval_expectation_set.expectations) == 30


def test_retrieval_expectation_set_covers_every_curated_question() -> None:
    question_set = load_evaluation_question_set()
    retrieval_expectation_set = load_retrieval_expectation_set()

    validate_retrieval_expectation_alignment(question_set, retrieval_expectation_set)


def test_grounded_questions_retain_retrieval_required_expectations() -> None:
    retrieval_expectation_set = load_retrieval_expectation_set()

    expectations = {
        expectation.question_id: expectation.retrieval_expectation
        for expectation in retrieval_expectation_set.expectations
    }

    for question_id in ["qa-001", "qa-006"]:
        assert expectations[question_id] == "grounded_retrieval_required"


def test_refusal_questions_retain_no_retrieval_expectations() -> None:
    retrieval_expectation_set = load_retrieval_expectation_set()

    expectations = {
        expectation.question_id: expectation.retrieval_expectation
        for expectation in retrieval_expectation_set.expectations
    }

    for question_id in ["scope-001", "scope-006", "inj-001", "inj-006"]:
        assert expectations[question_id] == "no_retrieval_expected"


def test_guardrail_questions_retain_guardrail_retrieval_expectations() -> None:
    retrieval_expectation_set = load_retrieval_expectation_set()

    expectations = {
        expectation.question_id: expectation.retrieval_expectation
        for expectation in retrieval_expectation_set.expectations
    }

    for question_id in ["cite-001", "cite-006", "conf-001", "conf-006"]:
        assert expectations[question_id] == "guardrail_retrieval_expected"


def test_invalid_retrieval_expectation_set_with_unknown_question_id_fails(
    tmp_path: Path,
) -> None:
    invalid_retrieval_expectation_path = tmp_path / "invalid-retrieval-expectations.json"
    invalid_retrieval_expectation_path.write_text(
        """
{
  "version": "invalid",
  "expectations": [
    {
      "question_id": "unknown-001",
      "retrieval_expectation": "grounded_retrieval_required"
    }
  ]
}
""".strip()
        + "\n",
        encoding="utf-8",
    )

    question_set = load_evaluation_question_set()
    retrieval_expectation_set = load_retrieval_expectation_set(
        invalid_retrieval_expectation_path
    )

    with pytest.raises(ValueError, match="unknown question ids"):
        validate_retrieval_expectation_alignment(question_set, retrieval_expectation_set)


def test_load_citation_expectation_set_returns_typed_dataset() -> None:
    citation_expectation_set = load_citation_expectation_set()

    assert isinstance(citation_expectation_set, CitationExpectationSet)
    assert citation_expectation_set.version == "2026-05-20-citation-expectations-v1"
    assert len(citation_expectation_set.expectations) == 30


def test_citation_expectation_set_covers_every_curated_question() -> None:
    question_set = load_evaluation_question_set()
    citation_expectation_set = load_citation_expectation_set()

    validate_citation_expectation_alignment(question_set, citation_expectation_set)


def test_grounded_questions_retain_citations_required_expectations() -> None:
    citation_expectation_set = load_citation_expectation_set()

    expectations = {
        expectation.question_id: expectation.citation_expectation
        for expectation in citation_expectation_set.expectations
    }

    for question_id in ["qa-001", "qa-006"]:
        assert expectations[question_id] == "citations_required"


def test_refusal_questions_retain_no_citation_expectations() -> None:
    citation_expectation_set = load_citation_expectation_set()

    expectations = {
        expectation.question_id: expectation.citation_expectation
        for expectation in citation_expectation_set.expectations
    }

    for question_id in ["scope-001", "scope-006", "inj-001", "inj-006"]:
        assert expectations[question_id] == "no_citations_expected"


def test_guardrail_questions_retain_guardrail_citation_posture() -> None:
    citation_expectation_set = load_citation_expectation_set()

    expectations = {
        expectation.question_id: expectation.citation_expectation
        for expectation in citation_expectation_set.expectations
    }

    for question_id in ["cite-001", "cite-006", "conf-001", "conf-006"]:
        assert expectations[question_id] == "guardrail_citation_posture"


def test_invalid_citation_expectation_set_with_unknown_question_id_fails(
    tmp_path: Path,
) -> None:
    invalid_citation_expectation_path = tmp_path / "invalid-citation-expectations.json"
    invalid_citation_expectation_path.write_text(
        """
{
  "version": "invalid",
  "expectations": [
    {
      "question_id": "unknown-001",
      "citation_expectation": "citations_required"
    }
  ]
}
""".strip()
        + "\n",
        encoding="utf-8",
    )

    question_set = load_evaluation_question_set()
    citation_expectation_set = load_citation_expectation_set(
        invalid_citation_expectation_path
    )

    with pytest.raises(ValueError, match="unknown question ids"):
        validate_citation_expectation_alignment(question_set, citation_expectation_set)


def test_evaluation_question_result_contract_validates() -> None:
    result = EvaluationQuestionResult(
        question_id="qa-001",
        status="matched",
        actual_behavior="normal_answer",
        expected_behavior="normal_answer",
        notes="Behavior matched expected outcome.",
    )

    assert result.question_id == "qa-001"
    assert result.status == "matched"


def test_evaluation_run_result_contract_validates() -> None:
    run_result = EvaluationRunResult(
        run_id="eval-run-001",
        question_set_version="2026-05-19-target-30-complete",
        golden_behavior_version="2026-05-19-golden-behaviors-v1",
        results=[
            EvaluationQuestionResult(
                question_id="qa-001",
                status="matched",
                actual_behavior="normal_answer",
                expected_behavior="normal_answer",
            )
        ],
    )

    assert run_result.run_id == "eval-run-001"
    assert run_result.results[0].question_id == "qa-001"


def test_evaluation_run_result_requires_unique_question_ids() -> None:
    with pytest.raises(ValueError, match="unique"):
        EvaluationRunResult(
            run_id="eval-run-002",
            question_set_version="2026-05-19-target-30-complete",
            golden_behavior_version="2026-05-19-golden-behaviors-v1",
            results=[
                EvaluationQuestionResult(
                    question_id="qa-001",
                    status="matched",
                    actual_behavior="normal_answer",
                    expected_behavior="normal_answer",
                ),
                EvaluationQuestionResult(
                    question_id="qa-001",
                    status="mismatched",
                    actual_behavior="scope_refusal",
                    expected_behavior="normal_answer",
                ),
            ],
        )
