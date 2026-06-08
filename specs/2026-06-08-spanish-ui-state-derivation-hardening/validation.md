# Validation

## Status

- Completed on `2026-06-08`.
- Checks passed:
  - `./.venv/bin/python -m ruff check app/ui.py tests/test_app_ui.py tests/test_guardrail_abuse_cases.py tests/test_smoke.py`
  - `./.venv/bin/python -m pytest tests/test_app_ui.py tests/test_guardrail_abuse_cases.py tests/test_smoke.py -q`

## Required Checks

- `./.venv/bin/python -m ruff check app/ui.py tests/test_app_ui.py tests/test_guardrail_abuse_cases.py tests/test_smoke.py`
- `./.venv/bin/python -m pytest tests/test_app_ui.py tests/test_guardrail_abuse_cases.py tests/test_smoke.py -q`

## Required Scenarios

- Spanish-facing backend/refusal wording does not break degraded/support state
  derivation.
- Existing success, refusal, and degraded UI paths still classify correctly.
- The hardening remains scoped to UI state derivation and does not drift into
  broader README/roadmap sync work.

## Merge Readiness

This spec is ready when the UI state derivation no longer depends on brittle
English backend substrings for:

- degraded answer-quality classification;
- support/refusal outcome classification;
- stable Spanish demo behavior under existing result contracts.
