# Validation

## Status

- Implementation complete on `2026-05-20`.
- Verification completed with:
  - `ruff check .`
  - `pytest`

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- Every curated evaluation question has a valid retrieval expectation record or
  an explicit no-retrieval expectation where appropriate.
- Grounded-QA questions retain explicit retrieval-oriented expectations.
- Unsupported-query and prompt-injection questions retain explicit limited or
  absent retrieval expectations.
- Citation and confidence guardrail questions retain explicit retrieval
  expectations consistent with guarded behavior.
- The slice remains scoped to retrieval expectations only.

## Merge Readiness

This spec is ready when the next `Phase 10` slice is decision-complete for:

- deterministic retrieval expectation coverage over the curated question set;
- explicit distinction between grounded and refusal/guardrail retrieval cases;
- locally reviewable, typed expectation structure;

without drifting into citation expectations or runner work.
