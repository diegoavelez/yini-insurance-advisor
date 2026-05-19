"""Independently callable policy comparison tool wrapper."""

from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Sequence

from contracts import (
    Clause,
    ComparisonItem,
    PolicyComparisonResult,
    PolicyComparisonToolResult,
    ToolError,
)
from ops.observability import log_timed_event

TOOL_LOGGER = logging.getLogger("yini.tools.policy_comparison")


def classify_policy_comparison_error(exc: Exception) -> ToolError:
    """Map policy comparison failures into the typed tool error surface."""

    if isinstance(exc, ValueError):
        return ToolError(kind="input_validation_failure", message=str(exc))
    return ToolError(kind="comparison_failure", message=str(exc))


def validate_policy_comparison_input(clauses: Sequence[Clause]) -> None:
    """Validate policy comparison input before processing."""

    if not isinstance(clauses, Sequence):
        raise ValueError("clauses must be a sequence of Clause items.")
    for clause in clauses:
        if not isinstance(clause, Clause):
            raise ValueError("clauses must contain only Clause items.")


def build_comparison_points(clauses: Sequence[Clause]) -> tuple[list[ComparisonItem], list[str]]:
    """Build conservative comparison points and insufficiency notes from clauses."""

    clauses_by_category: dict[str, list[Clause]] = defaultdict(list)
    for clause in clauses:
        clauses_by_category[clause.category].append(clause)

    comparison_points: list[ComparisonItem] = []
    notes: list[str] = []

    for category, category_clauses in clauses_by_category.items():
        source_documents = sorted({clause.document_name for clause in category_clauses})
        if len(source_documents) < 2:
            notes.append(
                f"Insufficient cross-document evidence to compare {category} clauses."
            )
            continue

        unique_summaries = list(dict.fromkeys(clause.summary for clause in category_clauses))
        if len(unique_summaries) == 1:
            finding = (
                f"{category.capitalize()} language is materially aligned across the "
                "compared documents."
            )
        else:
            finding = (
                f"{category.capitalize()} language differs across the compared documents."
            )

        comparison_points.append(
            ComparisonItem(
                criterion=f"{category}_comparison",
                finding=finding,
                source_documents=source_documents,
                sufficient_information=True,
            )
        )

    return comparison_points, notes


def policy_comparison_tool(
    clauses: Sequence[Clause],
    *,
    request_id: str | None = None,
) -> PolicyComparisonToolResult:
    """Compare typed clause evidence conservatively without performing retrieval."""

    try:
        with log_timed_event(
            TOOL_LOGGER,
            event_type="policy_comparison_tool",
            request_id=request_id,
            start_fields={"input_clause_count": len(clauses)},
            success_fields_factory=(
                lambda _duration_ms: {
                    "result_count": len(comparison_result.comparison_points),
                    "sufficient_information": comparison_result.sufficient_information,
                }
            ),
        ):
            validate_policy_comparison_input(clauses)
            comparison_points, notes = build_comparison_points(clauses)
            comparison_result = PolicyComparisonResult(
                comparison_points=comparison_points,
                sufficient_information=bool(comparison_points),
                notes=notes,
            )
            return PolicyComparisonToolResult(ok=True, result=comparison_result)
    except Exception as exc:
        return PolicyComparisonToolResult(ok=False, error=classify_policy_comparison_error(exc))
