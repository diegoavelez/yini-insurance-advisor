# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 9 — Guardrails`.

The goal is to add explicit scope guardrails for unsupported or out-of-scope
queries, so the system returns a conservative refusal outcome instead of
proceeding through the normal answer path.

This slice should stay focused on scope validation and refusal behavior only.
It should not introduce prompt-injection handling, abuse-case telemetry, or
broader confidence/citation guardrails.

## In Scope

- Add explicit unsupported-query scope validation.
- Add conservative refusal behavior for out-of-scope queries.
- Preserve typed response/workflow behavior for refusal outcomes.
- Preserve observability for refusal decisions.

## Out of Scope

- Prompt injection detection.
- Abuse-case scenario suites.
- Confidence consistency guardrails.
- Mandatory citation enforcement.
- MCP exposure.
- UI redesign beyond showing the refusal outcome.

## Execution Model

This slice should refine the current grounded QA path at the workflow and UI
boundary.

At minimum:

1. Supported insurance-document queries continue through the normal workflow.
2. Unsupported or out-of-scope queries are rejected early and conservatively.
3. Refusal remains a valid non-error outcome, not a runtime failure.
4. The refusal outcome is visible through the current typed response path.

## Scope Contract

Scope validation must be explicit and deterministic.

At minimum:

- unsupported queries should be recognized before normal answer synthesis;
- refusal should remain narrow and factual;
- refusal should not pretend evidence-based support exists when the query is
  out of scope.

## Refusal Contract

The refusal behavior must be explicit and typed.

At minimum:

- unsupported-query refusal should remain a valid non-error outcome;
- refusal should preserve low confidence and review messaging;
- refusal should not fabricate citations or evidence.

## Observability Contract

The current observability expectations should be preserved.

At minimum:

- refusal decisions should remain correlated to a request id when one is
  provided;
- structured refusal events should be emitted;
- refusal outcomes should remain distinguishable from workflow/runtime failures.

## Acceptance Criteria

- Unsupported or out-of-scope queries are rejected conservatively.
- Refusal remains a typed non-error outcome.
- Supported queries still execute the normal path.
- Refusal decisions are traceable in state or events.
- The slice stops before prompt-injection, citation, or broader confidence work.
