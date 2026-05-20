# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 10 — Evaluation Dataset`.

The goal is to add hosted-like citation regression smoke coverage over the
existing local evaluation runner and citation expectation assets.

This slice should stay focused on citation-regression smoke checks only. It
should not add broader performance benchmarking or DSPy optimization.

## In Scope

- Add hosted-like citation regression smoke coverage over the current local
  evaluation runner or adjacent runtime seam.
- Reuse the existing citation expectation assets.
- Keep the smoke deterministic and locally executable.

## Out of Scope

- Broad latency benchmarking.
- DSPy optimization.
- UI redesign.

## Citation Smoke Contract

Citation regression smokes must stay narrow and explicit.

At minimum:

- one hosted-like citation smoke path should exist;
- the smoke should produce a deterministic citation-oriented assertion surface;
- the smoke should remain locally executable and reviewable;
- the slice should avoid expanding into general evaluation analytics.

## Acceptance Criteria

- Hosted-like citation regression smoke coverage exists.
- The smoke remains deterministic and locally executable.
- The slice stops before DSPy optimization work.
