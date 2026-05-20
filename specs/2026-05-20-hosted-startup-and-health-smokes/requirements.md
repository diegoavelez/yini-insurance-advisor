# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 10 — Evaluation Dataset`.

The goal is to add hosted-like startup and health smoke coverage over the
existing app/runtime seams.

This slice should stay focused on startup and health verification only. It
should not yet add latency regression checks, citation regression checks, or
DSPy optimization.

## In Scope

- Add hosted-like startup smoke coverage for the current app entrypoint.
- Add hosted-like health/readiness smoke coverage for the current observability
  seam.
- Keep smoke behavior deterministic and locally executable.
- Reuse current startup/health helpers rather than adding a new deployment path.

## Out of Scope

- Latency regression checks.
- Citation regression checks.
- DSPy optimization.
- UI redesign.

## Smoke Contract

Hosted startup and health smokes must stay narrow and explicit.

At minimum:

- startup smoke should verify the app entrypoint can initialize without launch;
- health smoke should verify the hosted health status seam remains callable;
- readiness smoke should verify the readiness seam remains callable;
- smoke outputs should remain deterministic and locally reviewable.

## Acceptance Criteria

- Hosted-like startup smoke coverage exists.
- Hosted-like health/readiness smoke coverage exists.
- The slice stops before latency or citation regression smoke work.
