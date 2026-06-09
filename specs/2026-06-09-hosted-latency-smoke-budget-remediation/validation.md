# Validation

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.

## Required Checks

- `./.venv/bin/python -m ruff check core/evaluation_runner.py tests/test_smoke.py`
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ./.venv/bin/python -m pytest tests/test_smoke.py -q`

## Required Scenarios

- The default hosted latency smoke remains callable and returns the expected
  payload shape.
- Deterministic injected timing can prove a within-budget outcome.
- Deterministic injected timing can prove an over-budget outcome.

## Merge Readiness

This spec is ready when hosted latency smoke coverage no longer depends on
machine-specific wall-clock timing yet still preserves the default callable
operator-facing smoke path.

## Evidence

- `./.venv/bin/python -m ruff check core/evaluation_runner.py tests/test_smoke.py`
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ./.venv/bin/python -m pytest tests/test_smoke.py -q`

## Recorded Outcome

- The hosted latency smoke now accepts injectable evaluation/timer seams for
  deterministic budget assertions in tests.
- The default callable smoke path remains intact for local/operator use.
- The full `tests/test_smoke.py` file passes under plugin-autoload-disabled
  execution, including deterministic within-budget and over-budget coverage
  for the remediated hosted latency smoke.
