# Validation

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.

## Required Checks

- Focused lint and tests for retrieval contracts, Qdrant filter mapping, and
  retrieval-path regressions.

## Required Scenarios

- `document_type` filters map into the Qdrant query filter.
- `product` filters map into the Qdrant query filter.
- Combined supported filters continue to work together.

## Merge Readiness

This spec is ready when advisor-facing retrieval truthfully supports the same
curated metadata fields that the current corpus can already carry into indexed
payloads.

## Evidence

- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py contracts/tools.py specs/2026-06-09-document-metadata-filter-enablement`
- `./.venv/bin/python -m pytest tests/test_retrieval.py tests/test_contracts.py -q`

## Recorded Outcome

- Retrieval now maps curated `document_type` and `product` filters into the Qdrant query filter instead of rejecting them.
- Combined supported filters remain deterministic across `document_type`, `product`, `document_name`, and `version`.
- Focused retrieval and contract regression checks pass for the enabled metadata-filter surface.
