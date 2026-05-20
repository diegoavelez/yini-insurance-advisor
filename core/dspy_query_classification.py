"""Minimal DSPy query-classification module skeleton."""

from __future__ import annotations

import importlib
from collections.abc import Callable
from typing import Any

from contracts import (
    QueryClassificationOptimizationInput,
    QueryClassificationOptimizationOutput,
)
from core.prompt_guardrails import detect_prompt_injection_signals
from core.query_scope import classify_query_scope


def dspy_is_available() -> bool:
    """Return whether DSPy can be imported in the current environment."""

    return importlib.util.find_spec("dspy") is not None


def classify_query_with_baseline(
    optimization_input: QueryClassificationOptimizationInput,
) -> QueryClassificationOptimizationOutput:
    """Map one user query to the current deterministic classification baseline."""

    injection_decision = detect_prompt_injection_signals(optimization_input.user_query)
    if injection_decision.triggered:
        return QueryClassificationOptimizationOutput(
            expected_behavior="prompt_injection_refusal",
            rationale=injection_decision.reason,
        )

    scope_decision = classify_query_scope(optimization_input.user_query)
    if scope_decision.scope == "unsupported":
        return QueryClassificationOptimizationOutput(
            expected_behavior="scope_refusal",
            rationale=scope_decision.reason,
        )

    return QueryClassificationOptimizationOutput(
        expected_behavior="normal_answer",
        rationale="Query remains within the supported insurance-document classification scope.",
    )


class DSPyQueryClassificationModule:
    """Minimal builder for a future DSPy query-classification program."""

    def __init__(self, predictor_factory: Callable[[type[Any]], object] | None = None) -> None:
        self._predictor_factory = predictor_factory

    @staticmethod
    def input_model() -> type[QueryClassificationOptimizationInput]:
        """Return the typed input contract for this optimization seam."""

        return QueryClassificationOptimizationInput

    @staticmethod
    def output_model() -> type[QueryClassificationOptimizationOutput]:
        """Return the typed output contract for this optimization seam."""

        return QueryClassificationOptimizationOutput

    @staticmethod
    def baseline_classifier(
        optimization_input: QueryClassificationOptimizationInput,
    ) -> QueryClassificationOptimizationOutput:
        """Return the current deterministic baseline output for one query."""

        return classify_query_with_baseline(optimization_input)

    def build(self) -> object:
        """Build the minimal DSPy predictor skeleton when DSPy is available."""

        if not dspy_is_available():
            raise RuntimeError(
                "DSPy is not installed in the current environment; the skeleton contract "
                "exists, but the runtime module cannot be built yet."
            )

        dspy = importlib.import_module("dspy")

        class QueryClassificationSignature(dspy.Signature):  # type: ignore[misc]
            """Minimal DSPy signature for query classification."""

            user_query = dspy.InputField()
            expected_behavior = dspy.OutputField()
            rationale = dspy.OutputField()

        predictor_factory = self._predictor_factory or dspy.Predict
        return predictor_factory(QueryClassificationSignature)


def create_dspy_query_classification_module() -> DSPyQueryClassificationModule:
    """Create the minimal DSPy query-classification module wrapper."""

    return DSPyQueryClassificationModule()
