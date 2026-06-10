# Validation

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.

## Required Checks

- Focused lint and tests for the UI citation-rendering seam.

## Required Scenarios

- Citations render `source_pdf_relative_path` when available.
- Citations render cleanly when the relative path is absent.
- Existing citation metadata remains visible after the new field is added.

## Merge Readiness

This spec is ready when the public demo can surface truthful relative-path
traceability in rendered citations without broadening the UI change beyond the
current formatting seam.

## Evidence

- `./.venv/bin/python -m ruff check app/ui.py tests/test_app_ui.py specs/2026-06-09-citation-ui-relative-path-display`
- `./.venv/bin/python -m pytest tests/test_app_ui.py -q`

## Recorded Outcome

- The public citation renderer now surfaces `source_pdf_relative_path` with a stable Spanish label when the field is available.
- Citation rendering remains clean and unchanged for citations that do not carry the relative path.
- Focused UI regression coverage passes for both relative-path presence and absence cases.
