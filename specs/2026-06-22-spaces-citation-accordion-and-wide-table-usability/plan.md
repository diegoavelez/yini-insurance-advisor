# Plan

## Objective

Make the hosted Spaces review workspace less noisy by collapsing `Citas clave` into an accordion and improving the usability of wide Markdown tables.

## Affected files

- `app/ui.py`
- `tests/test_app_ui.py`
- `README.md`
- `docs/spaces-manual-qa-checklist.md`
- `specs/roadmap.md`
- `specs/2026-06-22-spaces-citation-accordion-and-wide-table-usability/requirements.md`
- `specs/2026-06-22-spaces-citation-accordion-and-wide-table-usability/validation.md`

## Assumptions

- The current backend response shape is already sufficient for the hosted review workflow.
- Gradio accordions plus scoped CSS remain enough for a narrow fix.
- A sticky first table column is a safe readability improvement for the current hosted tables.

## Risks

- Overly aggressive sticky-column CSS could make narrow tables look awkward.
- Moving citations into an accordion could conflict with older manual-QA wording if the docs are not updated alongside the UI.

## Steps

1. Add a dated spec bundle for the refinement slice.
2. Move `Citas clave` into a dedicated collapsed accordion in the answer column.
3. Add a stronger table-affordance hint and scoped sticky-column/scrollbar-gutter CSS.
4. Update focused UI regression coverage and the hosted manual-QA wording.
5. Record the slice in the roadmap as a post-completion MVP refinement.

## Verification strategy

- Run focused `pytest` coverage for `tests/test_app_ui.py`.
- Confirm the slice stays UI-only by checking the final diff surface.

