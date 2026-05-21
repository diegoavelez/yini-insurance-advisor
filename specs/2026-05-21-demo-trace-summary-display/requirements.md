# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 13 — Demo UI Hardening`.

The goal is to add a narrow user-visible trace summary surface to the current
demo UI using existing workflow and observability seams where available,
without yet exposing broader support/debug context.

This slice should stay focused on trace-summary display only.

## In Scope

- Add a user-visible trace summary surface to the current demo UI.
- Reuse current workflow and observability seams where available.
- Keep the trace summary concise and review-oriented.
- Preserve the current response fields and backend behavior.

## Out of Scope

- Broader debug-context exposure.
- Degraded-service messaging.
- Deployment work.
- Broader workflow redesign.

## Trace Summary Expectations

At minimum:

- the demo should expose a concise trace summary surface;
- the displayed trace should help the user understand how the answer was
  produced without exposing sensitive internals;
- the slice should remain narrow enough to support the next debug-context slice
  without reopening the trace-summary presentation.

## Acceptance Criteria

- A user-visible trace summary surface exists in the demo UI.
- The trace summary is concise and review-oriented.
- The slice stops before broader debug-context or degraded-service work.
- The implementation is narrow enough to support the next `Phase 13` slice
  directly.
