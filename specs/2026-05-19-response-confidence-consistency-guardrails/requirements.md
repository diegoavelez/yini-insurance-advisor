# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 9 — Guardrails`.

The goal is to enforce confidence consistency across typed response outputs, so
responses do not overstate certainty when upstream evidence or verification
signals are weaker.

This slice should stay focused on confidence consistency only. It should not
introduce prompt-injection handling, abuse-case suites, or new citation
presence policy.

## In Scope

- Add explicit confidence consistency checks across typed response outputs.
- Add conservative downgrade behavior when confidence signals are mismatched.
- Preserve typed non-error behavior for downgraded outcomes.
- Preserve observability for confidence-consistency guardrail decisions.

## Out of Scope

- Prompt injection detection.
- Abuse-case validation suites.
- New citation presence policy.
- MCP exposure.
- UI redesign beyond surfacing the downgraded outcome.

## Execution Model

This slice should refine the current answer-generation and workflow path.

At minimum:

1. Supported queries can still proceed through the normal path.
2. If response confidence is stronger than the available verification or
   evidence supports, the guardrail intervenes before that stronger confidence
   is surfaced.
3. The surfaced result becomes conservative and typed rather than an
   overconfident answer.
4. Confidence-consistency decisions remain observable.

## Confidence Consistency Contract

Confidence consistency enforcement must be explicit and deterministic.

At minimum:

- surfaced confidence should not exceed what verification and evidence support;
- mismatched confidence should be downgraded conservatively;
- the guardrail should not silently upgrade weak evidence into stronger
  certainty.

## Response Contract

The guarded outcome must remain explicit and typed.

At minimum:

- confidence-consistency intervention should remain a valid non-error outcome;
- the guarded result should preserve review messaging and limitations;
- downgraded output should remain conservative in confidence.

## Observability Contract

The current observability expectations should be preserved.

At minimum:

- confidence-consistency guardrail decisions should remain correlated to a
  request id when one is provided;
- structured guardrail events should be emitted;
- guardrail outcomes should remain distinguishable from workflow/runtime
  failures.

## Acceptance Criteria

- Overconfident responses are not surfaced unchanged when upstream signals are weaker.
- The system returns a conservative typed downgraded outcome instead.
- Confidence-consistency guardrail decisions are traceable in state or events.
- The slice stops before prompt-injection or abuse-case work.
