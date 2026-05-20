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

- Every curated evaluation question has a valid citation expectation record or
  an explicit no-citation expectation where appropriate.
- Grounded-QA questions retain explicit citation-oriented expectations.
- Unsupported-query and prompt-injection questions retain explicit absent
  citation expectations.
- Citation and confidence guardrail questions retain explicit citation posture
  expectations consistent with guarded behavior.
- The slice remains scoped to citation expectations only.

## Merge Readiness

This spec is ready when the next `Phase 10` slice is decision-complete for:

- deterministic citation expectation coverage over the curated question set;
- explicit distinction between grounded and refusal/guardrail citation cases;
- locally reviewable, typed expectation structure;

without drifting into runner work.
