# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 13 — Demo UI Hardening`.

The goal is to add a narrow user-visible support-context surface to the current
public demo UI so an advisor can understand the status and follow-up context of
a request without exposing broader operator-facing debug metadata.

This slice should stay focused on support-context display only.

## In Scope

- Add a user-visible support-context surface to the current demo UI.
- Reuse current request and observability seams where available.
- Keep the support context concise, review-oriented, and safe for advisor/demo
  visibility.
- Preserve the current answer-generation behavior and existing UI outputs.

## Out of Scope

- Broader operator-facing debug metadata exposure.
- Loading-state work.
- Error/degraded-service redesign.
- Workflow redesign.

## Support Context Expectations

At minimum:

- the demo should expose a concise support-context surface;
- the displayed support context should help a user understand the current
  request status and how to follow up if needed;
- the slice should remain narrow enough to support the next debug-metadata
  slice without reopening the user-visible support presentation.

## Acceptance Criteria

- A user-visible support-context surface exists in the demo UI.
- The support context is concise, review-oriented, and safe for demo exposure.
- The slice stops before broader debug-metadata or degraded-service work.
- The implementation is narrow enough to support the next `Phase 13` slice
  directly.
