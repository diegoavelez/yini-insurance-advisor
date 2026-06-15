# Validation

This slice is ready when deterministic manifest bookkeeping and artifact iteration live behind their own `rag` seam and batch command behavior remains unchanged.

## Status

- Completed on `2026-06-14`.
- Checks passed:
  - `./.venv/bin/python -m ruff check rag/ingestion.py rag/ingestion_artifacts.py rag/ingestion_batch.py tests/test_ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py specs/2026-06-15-rag-ingestion-artifact-assembly-and-skip-policy-seam-extraction specs/2026-06-15-rag-manifest-recording-and-artifact-iteration-seam-extraction --ignore E501`
  - `./.venv/bin/python -m pytest -q tests/test_ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py`

## Planned Checks

1. `./.venv/bin/python -m pytest -q tests/test_ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/ingestion_batch.py tests/test_ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py specs/2026-06-15-rag-manifest-recording-and-artifact-iteration-seam-extraction --ignore E501`

## Expected Evidence

- source PDFs, chunk artifacts, and embedding artifacts are still iterated in deterministic sorted order;
- ingestion, embedding, and indexing manifest records still carry the same fields and failure fallbacks;
- `rag.ingestion.py` still exposes compatibility wrappers for any names that tests import or patch directly.
