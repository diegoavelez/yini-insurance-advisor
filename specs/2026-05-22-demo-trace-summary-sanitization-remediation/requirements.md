# Requirements

## Feature Summary

This feature defines a corrective implementation slice for
`Phase 13 — Demo UI Hardening`.

The goal is to remediate the current trace-summary surface so explicit trace
items cannot expose sensitive or overly internal detail in the public demo UI.

This slice should stay focused on trace-summary sanitization only.

## In Scope

- Sanitize explicit trace-summary items before they are rendered in the demo UI.
- Preserve concise and review-oriented trace visibility for safe trace items.
- Fall back safely when explicit trace items are unsuitable for public display.
- Strengthen tests around public trace-safety behavior.

## Out of Scope

- Broader debug-metadata redesign.
- New backend trace contracts.
- Degraded-service messaging.
- Deployment work.

## Sanitization Expectations

At minimum:

- explicit trace items shown in the public demo must not expose sensitive
  internals;
- safe concise trace items may still be shown directly;
- unsafe or overly detailed trace items must be redacted or replaced;
- the resulting trace surface must remain understandable and review-oriented.

## Acceptance Criteria

- Explicit trace-summary items are sanitized before public display.
- Unsafe trace details are not exposed verbatim in the public demo UI.
- Safe concise trace items remain visible where appropriate.
- The slice closes the remaining `Phase 13` audit gap without reopening broader
  UI hardening work.
