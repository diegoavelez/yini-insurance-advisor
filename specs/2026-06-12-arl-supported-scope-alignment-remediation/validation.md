# Validation

## Status

- Planned on `2026-06-12`.

## Required Checks

- Deterministic supported-scope classification admits representative ARL/RUI
  insurance-document questions.
- The app query flow no longer rejects the representative ARL/RUI question as
  `unsupported_scope_refusal`.

## Required Scenarios

- `classify_query_scope()` returns `supported` for an ARL/RUI query.
- `run_query()` reaches the grounded-answer path for the same ARL/RUI query.
- A clearly unrelated non-insurance query still returns `unsupported`.

## Merge Readiness

This slice is ready when the deterministic supported-scope seam no longer
blocks ARL/RUI document questions that the retrieval layer already supports.
