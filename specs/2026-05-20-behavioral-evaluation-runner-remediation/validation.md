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

- Golden behavior ownership is unambiguous after the remediation.
- The local evaluation runner no longer derives observed behavior from the same
  fixture label used as the expected value.
- Run results expose explicit expectation-dataset versions.
- The slice remains scoped to evaluation seam correction only.

## Merge Readiness

This spec is ready when the corrective `Phase 10` slice is decision-complete
for:

- non-tautological behavior evaluation;
- explicit expectation ownership;
- explicit expectation-dataset linkage in run results;

without drifting into `Phase 11`.
