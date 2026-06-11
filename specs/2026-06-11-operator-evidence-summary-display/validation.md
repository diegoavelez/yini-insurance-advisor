# Validation

## Status

- Planned on `2026-06-11`.
- Completed on `2026-06-11`.

## Required Checks

- Focused lint and tests for the operator-facing evidence-summary rendering seam.

## Required Scenarios

- The summary renders document names for evidence-backed responses.
- The summary includes curated `document_type` and `product` values when
  available.
- The summary remains clean when no evidence is available.

## Merge Readiness

This spec is ready when operators can quickly identify the current evidence set
through a compact summary without broadening the change into a larger UI
redesign or interactive evidence browser.

## Evidence

- `./.venv/bin/python -m ruff check app/ui.py tests/test_app_ui.py specs/2026-06-11-operator-evidence-summary-display`
- `./.venv/bin/python -m pytest tests/test_app_ui.py -q`

## Recorded Outcome

- Passed. The operator-facing debug seam now includes a compact evidence
  summary with deduplicated document names and curated `document_type` /
  `product` values when present, plus empty-evidence coverage.
