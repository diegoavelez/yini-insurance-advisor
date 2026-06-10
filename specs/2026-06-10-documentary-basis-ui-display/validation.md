# Validation

## Status

- Planned on `2026-06-10`.
- Completed on `2026-06-10`.

## Required Checks

- Focused lint and tests for the documentary-basis UI rendering seam.

## Required Scenarios

- Documentary-basis entries render their stable source-review fields.
- Documentary-basis entries render optional relative-path traceability when available.
- The UI renders a clean fallback when documentary basis is empty.

## Merge Readiness

This spec is ready when the public demo exposes documentary-basis review data in
its own narrow UI surface without broadening the change into a larger layout
redesign.

## Evidence

- `./.venv/bin/python -m ruff check app/ui.py tests/test_app_ui.py tests/test_observability.py tests/test_guardrail_abuse_cases.py specs/2026-06-10-documentary-basis-ui-display`
- `./.venv/bin/python -m pytest tests/test_app_ui.py tests/test_observability.py tests/test_guardrail_abuse_cases.py -q`

## Recorded Outcome

- The public demo now exposes a dedicated documentary-basis output surface alongside citations.
- Documentary-basis rendering surfaces stable review fields, including optional relative-path traceability, while preserving a clean empty-state fallback.
- Focused UI, observability, and guardrail regression checks pass with the expanded UI output shape.
