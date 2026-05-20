"""Guardrail telemetry summary contracts."""

from __future__ import annotations

from pydantic import BaseModel, Field


class GuardrailEventRecord(BaseModel):
    """One narrow recorded guardrail/refusal event."""

    event_type: str = Field(min_length=1)
    request_id: str | None = None
    guardrail_surface: str | None = None
    timestamp_ms: int = Field(ge=0)
    details: dict[str, object] = Field(default_factory=dict)


class GuardrailSummary(BaseModel):
    """Compact local summary of recent guardrail/refusal activity."""

    total_events: int = Field(ge=0)
    event_counts: dict[str, int] = Field(default_factory=dict)
    recent_events: list[GuardrailEventRecord] = Field(default_factory=list)
