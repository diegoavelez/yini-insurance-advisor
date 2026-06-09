# Validation

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.

## Required Checks

- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`

## Required Scenarios

- `document_type` filter is rejected explicitly.
- `product` filter is rejected explicitly.
- Supported filters such as `document_name` and `version` continue to work.

## Merge Readiness

This spec is ready when the metadata-filter surface is truthful about what the
current corpus payload actually supports, and unsupported filters no longer
fail silently through empty retrieval results.

## Evidence

- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`

## Recorded Outcome

- Retrieval now rejects unsupported `document_type` and `product` filters
  explicitly before building a Qdrant filter.
- Supported filters backed by the current payload contract (`document_name` and
  `version`) remain functional.
- The metadata-filter surface no longer fails silently through empty retrieval
  behavior for unsupported corpus fields.
