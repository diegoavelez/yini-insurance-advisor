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

- A selected retryable workflow/tool failure is retried and then succeeds.
- A selected retryable workflow/tool failure exhausts retries and returns a
  typed terminal-failure workflow result.
- A non-retryable workflow/tool failure fails immediately without retry.
- Retry attempts remain observable and correlated when request ids are present.
- Terminal failure after retry exhaustion emits a distinct structured event.
- The implementation remains scoped to retry-policy work only.

## Merge Readiness

This spec is ready when the next `Phase 8` slice is decision-complete for:

- bounded retry behavior on selected workflow stages;
- typed terminal-failure behavior after retry exhaustion;
- preserved retry observability;

without drifting into broader recovery-tree work.
