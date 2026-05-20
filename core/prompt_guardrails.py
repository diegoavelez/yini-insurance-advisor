"""Deterministic prompt-injection signal detection for narrow refusal guardrails."""

from __future__ import annotations

import re

from pydantic import BaseModel, Field

INJECTION_SIGNAL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "ignore_previous_instructions",
        re.compile(r"(?i)\bignore\b.{0,40}\b(previous|prior|above)\b.{0,40}\binstructions?\b"),
    ),
    (
        "reveal_system_prompt",
        re.compile(r"(?i)\b(reveal|show|print|display)\b.{0,40}\b(system prompt|hidden prompt)\b"),
    ),
    (
        "bypass_guardrails",
        re.compile(r"(?i)\b(bypass|disable|override)\b.{0,40}\b(guardrails|safety|policies)\b"),
    ),
)


class PromptInjectionDecision(BaseModel):
    """Typed prompt-injection signal decision for one query."""

    triggered: bool
    signals: list[str] = Field(default_factory=list)
    reason: str = Field(min_length=1)


def detect_prompt_injection_signals(user_query: str) -> PromptInjectionDecision:
    """Return a deterministic injection-signal decision for one query."""

    matched_signals = [
        signal_name
        for signal_name, pattern in INJECTION_SIGNAL_PATTERNS
        if pattern.search(user_query)
    ]
    if matched_signals:
        return PromptInjectionDecision(
            triggered=True,
            signals=matched_signals,
            reason=(
                "Query matched a deterministic prompt-injection guardrail pattern and was "
                "refused conservatively."
            ),
        )
    return PromptInjectionDecision(
        triggered=False,
        signals=[],
        reason="No deterministic prompt-injection signals were detected.",
    )
