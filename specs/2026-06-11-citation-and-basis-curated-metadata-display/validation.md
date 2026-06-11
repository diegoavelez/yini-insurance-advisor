# Validation

## Status

- Planned on `2026-06-11`.
- Completed on `2026-06-11`.

## Required Checks

- Focused lint and tests for citation-facing contracts, grounded-answer
  propagation, and Gradio rendering seams.

## Required Scenarios

- Citations render `document_type` and `product` when available.
- Documentary-basis items render `document_type` and `product` when available.
- Citation-facing outputs remain clean when the curated metadata is absent.

## Merge Readiness

This spec is ready when curated retrieval metadata becomes visible in the
current operator-facing citation surfaces without broadening the change into
filter controls or a larger UI redesign.

## Evidence

- `./.venv/bin/python -m ruff check contracts/responses.py rag/ingestion.py app/ui.py tests/test_contracts.py tests/test_grounded_answer_generation.py tests/test_app_ui.py specs/2026-06-11-citation-and-basis-curated-metadata-display`
- `./.venv/bin/python -m pytest tests/test_contracts.py tests/test_grounded_answer_generation.py tests/test_app_ui.py -q`

## Recorded Outcome

- Citations and documentary-basis items now optionally carry curated `document_type` and `product` values when retrieval provides them.
- The current Gradio `Citas` and `Base documental` surfaces render those fields with stable Spanish labels while preserving clean fallbacks when metadata is absent.
- Focused contract, grounded-answer, and UI regression checks pass for the new curated-metadata display seam.
