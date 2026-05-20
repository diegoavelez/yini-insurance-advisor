"""Optimization dataset loading helpers."""

from __future__ import annotations

from pathlib import Path

from contracts import (
    EvaluationQuestionSet,
    GoldenBehaviorSet,
    QueryClassificationOptimizationDataset,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_QUERY_CLASSIFICATION_OPTIMIZATION_DATASET_PATH = (
    PROJECT_ROOT / "data" / "optimization" / "query-classification-subset.json"
)


def load_query_classification_optimization_dataset(
    path: Path = DEFAULT_QUERY_CLASSIFICATION_OPTIMIZATION_DATASET_PATH,
) -> QueryClassificationOptimizationDataset:
    """Load and validate the local query-classification optimization subset."""

    return QueryClassificationOptimizationDataset.model_validate_json(
        path.read_text(encoding="utf-8")
    )


def validate_query_classification_optimization_alignment(
    dataset: QueryClassificationOptimizationDataset,
    question_set: EvaluationQuestionSet,
    golden_behavior_set: GoldenBehaviorSet,
) -> None:
    """Validate optimization subset linkage to evaluation and golden assets."""

    questions_by_id = {question.question_id: question for question in question_set.questions}
    golden_by_id = {
        expectation.question_id: expectation.expected_behavior
        for expectation in golden_behavior_set.expectations
    }

    for example in dataset.examples:
        question = questions_by_id.get(example.source_question_id)
        if question is None:
            raise ValueError("optimization dataset contains unknown source question ids.")
        if example.user_query != question.prompt:
            raise ValueError("optimization dataset user_query must match the source question.")
        if example.category != question.category:
            raise ValueError("optimization dataset category must match the source question.")
        if golden_by_id.get(example.source_question_id) != example.expected_behavior:
            raise ValueError(
                "optimization dataset expected behavior must match the golden behavior set."
            )
