# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 13 — Demo UI Hardening`.

The goal is to add explicit degraded-service messaging for partial-answer and
reduced-quality response conditions that still return a draft in the public
demo UI, without reopening runtime-readiness degradation work.

This slice should stay focused on answer-quality degradation only.

## In Scope

- Add user-visible degraded-service messaging for partial-answer or reduced-
  quality draft conditions.
- Reuse the current grounded-answer, confidence, limitation, and guardrail seams
  where available.
- Keep degraded-service messaging concise and review-oriented.
- Preserve the current answer-generation behavior and existing readiness
  messaging.

## Out of Scope

- Runtime-readiness degradation messaging.
- Broader deployment work.
- Workflow redesign.
- New backend quality-evaluation pipelines.

## Answer-Quality Degradation Expectations

At minimum:

- the demo should expose explicit messaging when a draft is lower-confidence or
  otherwise quality-degraded but still returned;
- the messaging should help a user understand that the answer remains a draft
  requiring extra care;
- the slice should remain narrow enough to close `Phase 13` without reopening
  readiness degradation semantics.

## Acceptance Criteria

- A user-visible answer-quality degraded surface exists in the demo UI.
- Degraded-quality messaging is concise and review-oriented.
- The slice stops before broader deployment or backend quality redesign work.
- The implementation is narrow enough to close the remaining `Phase 13` work
  directly.
