# Requirements

## Feature Summary

This feature defines the final narrow implementation slice of `Phase 9 — Guardrails`.

The goal is to make guardrail-triggered refusal activity operationally visible
through a narrow summary surface, without changing the existing guardrail
heuristics.

This slice should stay focused on refusal telemetry and summary behavior only.
It should not add new detection rules or broaden into Phase 10 evaluation work.

## In Scope

- Persist or expose a narrow summary of guardrail/refusal events.
- Cover refusal-triggering guardrails already implemented in the system.
- Preserve deterministic, typed behavior for the summary surface.
- Preserve request-correlation where available.

## Out of Scope

- New prompt-injection heuristics.
- New scope-classification heuristics.
- New citation or confidence policy.
- Broader evaluation analytics.
- MCP exposure.
- UI redesign beyond a narrow operational summary surface.

## Execution Model

This slice should build on existing structured guardrail events.

At minimum:

1. Guardrail/refusal events already emitted by the system become reviewable through a narrow summary surface.
2. The summary stays deterministic and compact.
3. The summary distinguishes guardrail types and counts.
4. Request-correlation remains available where already present.

## Telemetry Contract

Telemetry behavior must stay explicit and narrow.

At minimum:

- summary data should derive from already-emitted guardrail/refusal events;
- guardrail types should remain distinguishable;
- the summary should not require a full observability platform.

## Summary Contract

The summary surface must remain deterministic and operationally useful.

At minimum:

- summary should expose guardrail type counts;
- summary should expose enough context to confirm which class of refusal occurred;
- summary should remain narrow and local to the current MVP runtime.

## Acceptance Criteria

- Guardrail/refusal telemetry is reviewable through a narrow summary surface.
- Guardrail classes remain distinguishable in the summary.
- Request correlation is preserved where present.
- The slice stops before broader evaluation or analytics work.
