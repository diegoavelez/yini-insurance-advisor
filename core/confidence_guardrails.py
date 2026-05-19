"""Confidence-consistency guardrails for typed response outputs."""

from __future__ import annotations

from contracts.responses import ConfidenceLevel


def enforce_confidence_consistency(
    proposed_confidence: ConfidenceLevel,
    *,
    has_cautionary_signals: bool,
    verification_supported: bool | None = None,
) -> tuple[ConfidenceLevel, bool]:
    """Return a conservative confidence level plus whether a downgrade occurred."""

    if verification_supported is False:
        return "low", proposed_confidence != "low"
    if proposed_confidence == "high" and has_cautionary_signals:
        return "medium", True
    return proposed_confidence, False
