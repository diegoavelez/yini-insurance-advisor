# Validation

## Status

- Implementation complete on `2026-05-19`.
- Verification completed with:
  - `ruff check .`
  - `pytest`

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- Every curated evaluation question has a linked golden expected behavior entry.
- Normal grounded-QA questions retain explicit non-guardrail expectations.
- Unsupported-query and prompt-injection questions retain explicit refusal expectations.
- Citation and confidence guardrail questions retain explicit guarded-outcome expectations.
- The slice remains scoped to behavior expectations only.

## Merge Readiness

This spec is ready when the next `Phase 10` slice is decision-complete for:

- golden expected behavior coverage over the curated question set;
- explicit refusal and guardrail outcomes;
- deterministic, reviewable dataset structure;

without drifting into retrieval/citation evidence annotations or runner work.
