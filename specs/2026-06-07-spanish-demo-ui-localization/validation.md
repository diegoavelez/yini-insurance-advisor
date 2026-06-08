# Validation

## Status

- Completed on `2026-06-07`.
- Checks passed:
  - `./.venv/bin/python -m ruff check app/ui.py tests/test_app_ui.py tests/test_guardrail_abuse_cases.py tests/test_observability.py tests/test_smoke.py`
  - `./.venv/bin/python -m pytest tests/test_app_ui.py -q`
  - `./.venv/bin/python -m pytest tests/test_guardrail_abuse_cases.py tests/test_observability.py tests/test_smoke.py -q`

## Required Checks

- `./.venv/bin/python -m ruff check .`
- `./.venv/bin/python -m pytest tests/test_app_ui.py`
- `./.venv/bin/python -m pytest tests/test_guardrail_abuse_cases.py`

## Required Scenarios

- The public Gradio labels are shown in Spanish.
- User-visible helper and status copy is shown in Spanish.
- Existing UI response surfaces remain present.
- Retrieval, scope, and backend answer behavior remain unchanged.

## Merge Readiness

This spec is ready when the first `Phase 15` slice is decision-complete for:

- Spanish-visible demo UI copy;
- stable preservation of the current response surfaces;
- no drift into retrieval or guardrail changes.
