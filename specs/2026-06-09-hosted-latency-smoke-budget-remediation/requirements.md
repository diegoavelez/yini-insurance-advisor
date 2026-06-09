# Requirements

## Feature Summary

This feature defines the third narrow slice of
`Phase 17 — Runtime Compatibility Hardening`.

The goal is to remove machine-dependent flakiness from the hosted latency smoke
so the repository can validate the latency contract deterministically while
still preserving one callable default smoke path.

## In Scope

- Refactor the hosted latency smoke helper so latency measurement can be
  injected deterministically in tests.
- Preserve the current callable default smoke payload for local/operator use.
- Add focused tests for within-budget and over-budget outcomes that do not rely
  on wall-clock timing of the current machine.

## Out of Scope

- Changing the evaluation dataset.
- Changing hosted query-classification latency validation behavior.
- Optimizing runtime performance of the local evaluation runner.
- Adjusting unrelated smoke payloads.

## Acceptance Criteria

- The hosted latency smoke can be exercised deterministically in tests through
  injected timing and evaluation-run seams.
- The callable smoke test no longer depends on the current machine completing
  the full evaluation runner under five seconds.
- Focused tests cover both within-budget and over-budget outcomes.
