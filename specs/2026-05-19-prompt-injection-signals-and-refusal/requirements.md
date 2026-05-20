# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 9 — Guardrails`.

The goal is to detect a narrow set of prompt-injection-like instructions and
return a conservative refusal outcome instead of allowing the system to proceed
through the normal answer path.

This slice should stay focused on deterministic injection signals and refusal
behavior only. It should not yet add abuse-case suites or broader telemetry
expansion.

## In Scope

- Add explicit prompt-injection signal detection for a narrow deterministic rule set.
- Add conservative refusal behavior when those signals trigger.
- Preserve typed non-error behavior for injection-triggered refusals.
- Preserve observability for prompt-injection guardrail decisions.

## Out of Scope

- Broader prompt security heuristics.
- Abuse-case validation suites.
- New citation or confidence policy.
- MCP exposure.
- UI redesign beyond showing the refusal outcome.

## Execution Model

This slice should refine the current query entry path.

At minimum:

1. Supported benign insurance-document queries can still proceed through the normal path.
2. Queries matching a narrow injection-signal rule set are rejected early and conservatively.
3. The refusal remains a valid typed non-error outcome, not a runtime failure.
4. Prompt-injection guardrail decisions remain observable.

## Injection Signal Contract

Injection-signal detection must be explicit and deterministic.

At minimum:

- the slice should rely on a small documented rule set, not a hidden heuristic cloud;
- triggered signals should be strong enough to justify conservative refusal;
- the slice should not attempt full jailbreak defense coverage yet.

## Refusal Contract

The refusal behavior must remain explicit and typed.

At minimum:

- injection-triggered refusal should remain a valid non-error outcome;
- refusal should preserve low confidence and review messaging;
- refusal should not surface answer-like supported content.

## Observability Contract

The current observability expectations should be preserved.

At minimum:

- prompt-injection guardrail decisions should remain correlated to a request id when one is provided;
- structured guardrail events should be emitted;
- guardrail outcomes should remain distinguishable from workflow/runtime failures.

## Acceptance Criteria

- Narrow prompt-injection signals trigger conservative refusal.
- Benign supported queries still execute the normal path.
- Injection-triggered refusal remains a typed non-error outcome.
- Prompt-injection guardrail decisions are traceable in state or events.
- The slice stops before abuse-case-suite work.
