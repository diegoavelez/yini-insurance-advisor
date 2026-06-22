# Validation

This slice is ready when the hosted Spaces UI keeps the answer as the primary visible surface while preserving easy access to citations and making wide tables easier to inspect.

## Acceptance checks

- A committed spec bundle exists for `spaces-citation-accordion-and-wide-table-usability`.
- The Gradio app layout exposes `Citas clave` as a collapsed accordion.
- The answer surface includes a visible table-affordance hint.
- Scoped CSS reserves stable scrollbar space where supported and makes the first table column sticky.
- Focused UI tests pass.
- The slice remains limited to the UI/documentation surface.

## Verification commands

- `PYTHONPATH=. ./.venv/bin/pytest tests/test_app_ui.py -q`
