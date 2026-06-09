# Validation

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.

## Required Checks

- `./.venv/bin/python -m ruff check contracts/documents.py contracts/embeddings.py rag/ingestion.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
- `./.venv/bin/python -m pytest tests/test_qdrant_indexing.py tests/test_retrieval.py -q`

## Required Scenarios

- New vector payloads include `source_pdf_relative_path`.
- Retrieval maps the field when present.
- Retrieval remains compatible with payloads that do not include the field.

## Merge Readiness

This spec is ready when raw-source relative path traceability survives the
current chunk → embedding → Qdrant → retrieval path without breaking older
payload compatibility.

## Evidence

- `./.venv/bin/python -m ruff check contracts/documents.py contracts/embeddings.py rag/ingestion.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
- `./.venv/bin/python -m pytest tests/test_qdrant_indexing.py tests/test_retrieval.py -q`

## Recorded Outcome

- `source_pdf_relative_path` now propagates through vector payload creation and
  persisted Qdrant payload mapping.
- Retrieved chunks now expose `source_pdf_relative_path` when the payload
  includes it.
- Retrieval remains compatible with older payloads that do not yet include the
  field.
