# Validation

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.

## Required Checks

- Focused lint and tests for response contracts, citation/documentary-basis
  mapping, and compatibility with older retrieval payloads.

## Required Scenarios

- Citations receive `source_pdf_relative_path` when available.
- Documentary-basis items receive `source_pdf_relative_path` when available.
- Citation-facing outputs remain valid when the relative path is absent.

## Merge Readiness

This spec is ready when operator-facing answer artifacts can expose truthful
relative-path traceability without changing the broader retrieval or answer
contracts.

## Evidence

- `./.venv/bin/python -m ruff check contracts/responses.py rag/ingestion.py tests/test_grounded_answer_generation.py tests/test_contracts.py specs/2026-06-09-citation-relative-path-traceability`
- `./.venv/bin/python -m pytest tests/test_grounded_answer_generation.py tests/test_contracts.py -q`

## Recorded Outcome

- Citations and documentary-basis items now optionally carry `source_pdf_relative_path` when retrieval provides it.
- Grounded-answer mapping preserves relative-path traceability without breaking contract compatibility for older payloads where the field is absent.
- Focused contract and grounded-answer regressions pass for the new citation-facing traceability seam.
