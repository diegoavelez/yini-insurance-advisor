# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 13 — Demo UI Hardening`.

The goal is to add explicit degraded-service messaging for runtime-readiness and
missing-dependency conditions in the public demo UI, without yet addressing
answer-quality degradation messaging.

This slice should stay focused on readiness-related degradation only.

## In Scope

- Add user-visible degraded-service messaging for runtime-readiness problems.
- Reuse the current readiness and dependency-availability seams where possible.
- Keep degraded-service messaging concise and understandable for demo users.
- Preserve the current answer-generation behavior when the runtime is healthy.

## Out of Scope

- Answer-quality degradation messaging.
- Broader deployment work.
- Workflow redesign.
- New backend readiness systems.

## Readiness Degradation Expectations

At minimum:

- the demo should expose explicit messaging for runtime-readiness problems;
- the messaging should help a user understand when the demo is not fully ready;
- the slice should remain narrow enough to support the next answer-quality
  degradation slice without reopening readiness messaging.

## Acceptance Criteria

- A user-visible readiness-degraded surface exists in the demo UI.
- Readiness degradation messaging is concise and understandable.
- The slice stops before answer-quality degradation work.
- The implementation is narrow enough to support the next `Phase 13` slice
  directly.
