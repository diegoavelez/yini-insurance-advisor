# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 13 — Demo UI Hardening`.

The goal is to add a narrow operator-facing debug-metadata surface to the
current public demo UI while preserving a clear boundary from the existing
user-visible support context.

This slice should stay focused on debug-metadata exposure only.

## In Scope

- Add an operator-facing debug-metadata surface to the current demo UI.
- Reuse current observability and request-correlation seams where available.
- Keep the metadata compact, explicit, and operationally useful.
- Preserve the current answer-generation behavior and existing user-visible
  outputs.

## Out of Scope

- Broader degraded-service messaging.
- Loading-state work.
- Workflow redesign.
- New backend observability pipelines.

## Debug Metadata Expectations

At minimum:

- the demo should expose a compact debug-metadata surface;
- the displayed metadata should help an operator inspect request execution
  without replacing broader observability tooling;
- the slice should remain narrow enough to support the next loading/error-state
  slice without reopening the support/debug boundary.

## Acceptance Criteria

- An operator-facing debug-metadata surface exists in the demo UI.
- The metadata is compact, explicit, and clearly separate from the user-visible
  support context.
- The slice stops before degraded-service messaging or loading/error-state work.
- The implementation is narrow enough to support the next `Phase 13` slice
  directly.
