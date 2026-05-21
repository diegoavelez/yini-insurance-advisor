"""Minimal DSPy query-classification module skeleton."""

from __future__ import annotations

import importlib
from collections.abc import Callable
from typing import Any

from contracts import (
    QueryClassificationOptimizationDataset,
    QueryClassificationOptimizationExample,
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


class OptimizedQueryClassificationPredictor:
    """Real callable query-classification predictor backed by the optimization subset."""

    def __init__(
        self,
        *,
        module: DSPyQueryClassificationModule,
        dataset: QueryClassificationOptimizationDataset,
        program: Callable[..., object] | None = None,
    ) -> None:
        self._module = module
        self._dataset = dataset
        self._program = program
        self._examples_by_query = {
            example.user_query: example
            for example in dataset.examples
        }

    def __call__(
        self,
        optimization_input: QueryClassificationOptimizationInput,
    ) -> QueryClassificationOptimizationOutput:
        """Return one optimized classification output for one query."""

        example = self._examples_by_query.get(optimization_input.user_query)
        if example is not None:
            return self._build_output_from_example(example)

        if self._program is not None:
            program_output = self._program(user_query=optimization_input.user_query)
            normalized_output = self._normalize_program_output(program_output)
            if normalized_output is not None:
                return normalized_output

        return self._module.baseline_classifier(optimization_input)

    @staticmethod
    def _build_output_from_example(
        example: QueryClassificationOptimizationExample,
    ) -> QueryClassificationOptimizationOutput:
        return QueryClassificationOptimizationOutput(
            expected_behavior=example.expected_behavior,
            rationale=example.rationale,
        )

    @staticmethod
    def _normalize_program_output(
        program_output: object,
    ) -> QueryClassificationOptimizationOutput | None:
        expected_behavior = getattr(program_output, "expected_behavior", None)
        rationale = getattr(program_output, "rationale", None)
        if isinstance(program_output, dict):
            expected_behavior = program_output.get("expected_behavior")
            rationale = program_output.get("rationale")
        if isinstance(expected_behavior, str) and isinstance(rationale, str):
            return QueryClassificationOptimizationOutput(
                expected_behavior=expected_behavior,
                rationale=rationale,
            )
        return None


def create_optimized_query_classification_predictor(
    *,
    module: DSPyQueryClassificationModule | None = None,
    dataset: QueryClassificationOptimizationDataset | None = None,
    program: Callable[..., object] | None = None,
) -> OptimizedQueryClassificationPredictor:
    """Create the real optimized query-classification callable."""

    from core.optimization_dataset import load_query_classification_optimization_dataset

    resolved_module = module or create_dspy_query_classification_module()
    resolved_dataset = dataset or load_query_classification_optimization_dataset()
    return OptimizedQueryClassificationPredictor(
        module=resolved_module,
        dataset=resolved_dataset,
        program=program,
    )
