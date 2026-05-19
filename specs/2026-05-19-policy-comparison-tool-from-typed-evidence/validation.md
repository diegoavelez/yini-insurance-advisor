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

- Successful comparison returns structured comparison points.
- Insufficient information remains a valid non-error result.
- Comparison points remain traceable to source evidence.
- Validation/runtime failures return typed error information.
- Tool execution remains observable and correlated when request ids are present.
- The implementation remains scoped to policy comparison only.

## Merge Readiness

This spec is ready when the next `Phase 7` slice is decision-complete for:

- independently callable policy comparison behavior;
- structured comparison outputs and failure contracts;
- preserved observability expectations;

without drifting into citation verification, drafting, or orchestration work.
