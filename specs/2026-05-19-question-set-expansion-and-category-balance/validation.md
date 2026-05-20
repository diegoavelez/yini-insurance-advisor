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

- The expanded dataset validates against the existing evaluation schema.
- The total question set grows beyond the initial seed set.
- Grounded-QA coverage is expanded.
- Guardrail-oriented coverage is expanded across existing categories.
- The slice remains scoped to dataset expansion and balance only.

## Merge Readiness

This spec is ready when the next `Phase 10` slice is decision-complete for:

- a materially expanded curated question set;
- broader and more balanced category coverage;
- preserved typed schema validation;

without drifting into golden outputs or runner execution.
