# Validation

## Status

- Completed on `2026-05-20`.
- Checks passed:
  - `./.venv/bin/python -m ruff check .`
  - `./.venv/bin/python -m pytest tests/test_hosted_query_classification_latency.py tests/test_query_classification_latency.py`
  - `./.venv/bin/python -m pytest`

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- A hosted-like latency-budget validation seam exists.
- The result explicitly states whether the optimized path is within budget.
- The result exposes the budget threshold and observed hosted-like latency used
  for the decision.
- The slice remains scoped to hosted-like latency-budget validation only.

## Merge Readiness

This spec is ready when the remaining `Phase 11` latency gap is closed for:

- measurable hosted-like query-classification latency-budget validation;
- explicit within-budget / over-budget reporting;
- stable distinction between local comparison timing and product-facing request
  timing;

without drifting into broader productionization work.
