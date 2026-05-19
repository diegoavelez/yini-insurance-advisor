# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 9 — Guardrails`.

The goal is to enforce citation presence for answerable responses, so the
system does not return an apparently supported answer without at least one
traceable citation.

This slice should stay focused on citation presence only. It should not yet add
broader confidence-policy checks, prompt-injection handling, or abuse-case
telemetry.

## In Scope

- Add explicit citation presence checks for answerable responses.
- Add conservative fallback behavior when an answerable response lacks citations.
- Preserve typed non-error behavior for downgraded or limited responses.
- Preserve observability for citation-presence guardrail decisions.

## Out of Scope

- Confidence consistency policy.
- Prompt injection detection.
- Abuse-case scenario suites.
- Broader refusal telemetry beyond citation-presence decisions.
- MCP exposure.
- UI redesign beyond showing the downgraded outcome.

## Execution Model

This slice should refine the current answer-generation and workflow path.

At minimum:

1. Supported queries can still proceed through the normal path.
2. If an answerable response would be returned without citations, the guardrail
   intervenes before that answer is surfaced.
3. The surfaced result becomes conservative and typed rather than an unguarded
   answer.
4. Citation-presence guardrail decisions remain observable.

## Citation Presence Contract

Citation presence enforcement must be explicit and deterministic.

At minimum:

- answerable responses should include at least one traceable citation;
- if no citation is present, the response should be downgraded into a
  conservative limited outcome rather than pretending grounded support exists;
- the guardrail should not fabricate citations.

## Response Contract

The guarded outcome must remain explicit and typed.

At minimum:

- citation-presence intervention should remain a valid non-error outcome;
- the guarded result should preserve review messaging;
- guarded output should remain conservative in confidence and limitations.

## Observability Contract

The current observability expectations should be preserved.

At minimum:

- citation-presence guardrail decisions should remain correlated to a request id
  when one is provided;
- structured guardrail events should be emitted;
- guardrail outcomes should remain distinguishable from workflow/runtime
  failures.

## Acceptance Criteria

- Answerable responses without citations are not surfaced unguarded.
- The system returns a conservative typed guarded outcome instead.
- No citations are fabricated.
- Citation-presence guardrail decisions are traceable in state or events.
- The slice stops before confidence-policy or prompt-injection work.
