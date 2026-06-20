# Validation

This slice is ready when the hosted Space answer surface can render wide Markdown tables with horizontal scrolling and without shrinking the font.

## Acceptance checks

- A committed spec bundle exists for `spaces-wide-table-scroll-and-readability`.
- The Gradio app build includes a scoped CSS block for answer-surface tables.
- The answer markdown component carries the expected styling class.
- Focused UI tests pass.
- The slice remains limited to the UI layer.

## Verification commands

- `PYTHONPATH=. ./.venv/bin/pytest tests/test_app_ui.py -q`
