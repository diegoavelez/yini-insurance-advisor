# Requirements

## Feature Summary

This feature defines the remaining narrow implementation slice of
`Phase 6 — Baseline Observability`.

The goal is to make the current MVP operationally inspectable in hosted and
local runs through explicit latency-oriented traces, health/readiness checks,
and narrow Phoenix activation when configured.

This slice should build directly on the existing startup diagnostics and request
correlation work without expanding into broader observability platforms or
advanced dashboards.

## In Scope

- Add retrieval and grounded-answer latency traces.
- Add narrow hosted health and readiness checks for the MVP runtime path.
- Add conditional Phoenix activation when configured.
- Expose smoke-visible observability for the hosted app startup path.
- Keep the implementation minimal, operational, and testable.

## Out of Scope

- Distributed tracing systems.
- Full metrics backends.
- Cost dashboards.
- Deep performance analytics beyond the current runtime path.
- Tool-level observability for future Phase 7 tooling.

## Execution Model

This slice should cover the current runtime surfaces only:

1. Gradio app startup.
2. Gradio request path for retrieval and grounded answering.
3. Hosted smoke visibility through narrow health/readiness behavior.

It should not introduce new product capabilities beyond observability and
operational checks.

## Retrieval Trace Contract

This slice should make the current retrieval and answer-generation path
measurably inspectable.

At minimum:

- retrieval execution should emit duration information;
- grounded-answer execution should emit duration information;
- duration information should remain correlated to the request id introduced in
  the prior slice;
- traces should remain structured and machine-readable.

The trace shape may extend the current event model but should stay narrow and
consistent with the existing structured logging approach.

## Health / Readiness Contract

This slice should add the minimum hosted checks needed to make the MVP deploy
path operationally trustworthy.

At minimum:

- one health signal should confirm the app process is alive;
- one readiness signal should confirm the app is configured enough to serve the
  current grounded QA path;
- readiness must fail loudly when required runtime dependencies or required
  settings for the current MVP path are unavailable.

These checks should remain narrow and operational; they are not a user-facing
feature.

## Phoenix Activation Contract

If Phoenix configuration is present and enabled for this runtime path:

- the app should activate narrow Phoenix integration for hosted tracing;
- the implementation should remain optional and must not break runs where
  Phoenix is not configured;
- the activation path must not log secrets.

If Phoenix is not configured, the runtime should continue normally.

## Failure Behavior

If readiness checks fail:

- the failure must be explicit and observable;
- the app must not pretend to be ready;
- logs should preserve structured context for diagnosis.

If Phoenix activation fails:

- the failure policy must be explicit in the spec and implementation;
- it may either fail startup or degrade cleanly, but the behavior must be
  deliberate and testable.

## Acceptance Criteria

- Retrieval and grounded-answer durations are visible in structured traces.
- Health and readiness checks exist for the hosted MVP path.
- Hosted readiness fails explicitly when required runtime dependencies or
  settings are unavailable.
- Phoenix activation is optional and conditional on configuration.
- The slice stops before broader metrics or observability platform work.
