"""Local deterministic evaluation runner over curated evaluation assets."""

from __future__ import annotations

from contracts.evaluation import EvaluationQuestionResult, EvaluationRunResult
from core.evaluation_dataset import (
    load_citation_expectation_set,
    load_evaluation_question_set,
    load_golden_behavior_set,
    load_retrieval_expectation_set,
    validate_citation_expectation_alignment,
    validate_golden_behavior_alignment,
    validate_retrieval_expectation_alignment,
)


def run_local_evaluation() -> EvaluationRunResult:
    """Execute the narrow local evaluation runner over the current assets."""

    question_set = load_evaluation_question_set()
    golden_behavior_set = load_golden_behavior_set()
    retrieval_expectation_set = load_retrieval_expectation_set()
    citation_expectation_set = load_citation_expectation_set()

    validate_golden_behavior_alignment(question_set, golden_behavior_set)
    validate_retrieval_expectation_alignment(question_set, retrieval_expectation_set)
    validate_citation_expectation_alignment(question_set, citation_expectation_set)

    golden_expectations = {
        expectation.question_id: expectation.expected_behavior
        for expectation in golden_behavior_set.expectations
    }

    results: list[EvaluationQuestionResult] = []
    for question in question_set.questions:
        expected_behavior = golden_expectations[question.question_id]
        actual_behavior = question.expected_behavior
        status = "matched" if actual_behavior == expected_behavior else "mismatched"
        results.append(
            EvaluationQuestionResult(
                question_id=question.question_id,
                status=status,
                actual_behavior=actual_behavior,
                expected_behavior=expected_behavior,
                notes="Deterministic local asset-level evaluation run.",
            )
        )

    return EvaluationRunResult(
        run_id=(
            f"local-eval:{question_set.version}:"
            f"{golden_behavior_set.version}:{retrieval_expectation_set.version}:"
            f"{citation_expectation_set.version}"
        ),
        question_set_version=question_set.version,
        golden_behavior_version=golden_behavior_set.version,
        results=results,
    )
