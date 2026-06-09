# Validation

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.

## Required Checks

- Focused lint and tests for the ingestion, embedding-payload, and retrieval
  seams affected by curated metadata overlays.

## Required Scenarios

- Overlay metadata is applied when a matching stable document id exists.
- Missing overlay entries do not break ingestion.
- Curated `document_type` and `product` values survive into the indexed payload
  seam where future supported filters can use them.

## Merge Readiness

This spec is ready when the repository has a truthful, operator-controlled path
for adding retrieval-facing document metadata without relying on brittle
heuristics.

## Evidence

- `./.venv/bin/python -m ruff check contracts/__init__.py contracts/documents.py contracts/embeddings.py contracts/ingestion.py rag/ingestion.py tests/test_ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
- `./.venv/bin/python -m pytest tests/test_ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py tests/test_retrieval.py -q`

## Recorded Outcome

- The ingestion CLI now accepts an optional operator-curated metadata overlay
  keyed by stable `source_pdf_id`.
- Curated `document_type` and `product` values propagate through processed
  documents, chunk bundles, embedding payloads, Qdrant payloads, and retrieved
  chunk results.
- Documents without overlay entries continue to ingest successfully with no
  required manual metadata.
