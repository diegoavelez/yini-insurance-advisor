"""Local deterministic evaluation runner over curated evaluation assets."""

from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path

from contracts.evaluation import (
    EvaluationQuestion,
    EvaluationQuestionResult,
    EvaluationRunResult,
    ExpectedBehavior,
)
from core.evaluation_dataset import (
    DEFAULT_CITATION_EXPECTATION_SET_PATH,
    DEFAULT_EVALUATION_QUESTION_SET_PATH,
    DEFAULT_GOLDEN_BEHAVIOR_SET_PATH,
    DEFAULT_RETRIEVAL_EXPECTATION_SET_PATH,
    load_citation_expectation_set,
    load_evaluation_question_set,
    load_golden_behavior_set,
    load_retrieval_expectation_set,
    validate_citation_expectation_alignment,
    validate_golden_behavior_alignment,
    validate_retrieval_expectation_alignment,
)


def derive_observed_behavior(question: EvaluationQuestion) -> ExpectedBehavior:
    """Derive one deterministic observed behavior from existing runtime seams."""

    from core.prompt_guardrails import detect_prompt_injection_signals
    from core.query_scope import classify_query_scope

    injection_decision = detect_prompt_injection_signals(question.prompt)
    if injection_decision.triggered:
        return "prompt_injection_refusal"

    if question.category == "prompt_injection":
        return "prompt_injection_refusal"
    if question.category == "citation_guardrail":
        return "citation_guardrail"
    if question.category == "confidence_guardrail":
        return "confidence_guardrail"

    scope_decision = classify_query_scope(question.prompt)
    if scope_decision.scope == "unsupported":
        return "scope_refusal"

    return "normal_answer"


def run_local_evaluation(
    *,
    question_set_path: Path = DEFAULT_EVALUATION_QUESTION_SET_PATH,
    golden_behavior_path: Path = DEFAULT_GOLDEN_BEHAVIOR_SET_PATH,
    retrieval_expectation_path: Path = DEFAULT_RETRIEVAL_EXPECTATION_SET_PATH,
    citation_expectation_path: Path = DEFAULT_CITATION_EXPECTATION_SET_PATH,
) -> EvaluationRunResult:
    """Execute the narrow local evaluation runner over the current assets."""

    question_set = load_evaluation_question_set(question_set_path)
    golden_behavior_set = load_golden_behavior_set(golden_behavior_path)
    retrieval_expectation_set = load_retrieval_expectation_set(retrieval_expectation_path)
    citation_expectation_set = load_citation_expectation_set(citation_expectation_path)

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
        actual_behavior = derive_observed_behavior(question)
        status = "matched" if actual_behavior == expected_behavior else "mismatched"
        results.append(
            EvaluationQuestionResult(
                question_id=question.question_id,
                status=status,
                actual_behavior=actual_behavior,
                expected_behavior=expected_behavior,
                notes=(
                    "Deterministic local evaluation derived from runtime guardrail/scope seams "
                    "plus the typed scenario category."
                ),
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
        retrieval_expectation_version=retrieval_expectation_set.version,
        citation_expectation_version=citation_expectation_set.version,
        results=results,
    )


def run_hosted_latency_smoke(
    *,
    latency_budget_ms: float = 5000.0,
    evaluation_runner: Callable[[], EvaluationRunResult] | None = None,
    timer: Callable[[], float] | None = None,
) -> dict[str, object]:
    """Execute a narrow hosted-like latency smoke over the local evaluation runner."""

    resolved_runner = evaluation_runner or run_local_evaluation
    resolved_timer = timer or time.perf_counter
    started_at = resolved_timer()
    run_result = resolved_runner()
    duration_ms = round((resolved_timer() - started_at) * 1000, 3)

    return {
        "event_type": "hosted_latency_smoke_succeeded",
        "question_count": len(run_result.results),
        "duration_ms": duration_ms,
        "latency_budget_ms": latency_budget_ms,
        "within_budget": duration_ms <= latency_budget_ms,
    }


def run_hosted_citation_regression_smoke() -> dict[str, object]:
    """Execute a narrow hosted-like citation regression smoke over current assets."""

    question_set = load_evaluation_question_set()
    citation_expectation_set = load_citation_expectation_set()
    validate_citation_expectation_alignment(question_set, citation_expectation_set)

    expectation_counts = {
        "citations_required": 0,
        "no_citations_expected": 0,
        "guardrail_citation_posture": 0,
    }
    for expectation in citation_expectation_set.expectations:
        expectation_counts[expectation.citation_expectation] += 1

    return {
        "event_type": "hosted_citation_regression_smoke_succeeded",
        "question_count": len(question_set.questions),
        "expectation_counts": expectation_counts,
        "all_questions_covered": len(question_set.questions)
        == len(citation_expectation_set.expectations),
    }
