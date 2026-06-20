# Plan

## Objective

Make wide hosted answer tables readable by adding scoped horizontal-scroll styling to the Markdown answer surface.

## Affected files

- `app/ui.py`
- `tests/test_app_ui.py`
- `specs/2026-06-20-spaces-wide-table-scroll-and-readability/requirements.md`
- `specs/2026-06-20-spaces-wide-table-scroll-and-readability/validation.md`
- `specs/roadmap.md`

## Assumptions

- The issue is in Gradio Markdown rendering, not in answer generation.
- `elem_classes` plus `Blocks(css=...)` is sufficient for a narrow fix.

## Risks

- Overbroad CSS could affect non-tabular Markdown.
- Overly aggressive `white-space` rules could make very long textual cells awkward.

## Steps

1. Add a scoped CSS block for answer/documentary markdown tables.
2. Attach styling classes to the relevant Markdown components.
3. Add focused UI tests for the CSS/class wiring.
4. Update roadmap traceability for the new UX slice.

## Verification strategy

- Run focused `pytest` coverage for `tests/test_app_ui.py`.
- Recheck the hosted SOAT tariff response after redeploy.
