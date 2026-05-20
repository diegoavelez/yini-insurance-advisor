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

- The evaluation schema validates the curated question entries.
- The initial set includes normal grounded-QA prompts.
- The initial set includes unsupported-query prompts.
- The initial set includes prompt-injection-oriented prompts.
- The initial set remains scoped to schema and question authoring only.

## Merge Readiness

This spec is ready when the first `Phase 10` slice is decision-complete for:

- typed evaluation question schemas;
- an initial curated question set;
- schema validation coverage;

without drifting into golden outputs or runner execution.
