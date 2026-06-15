# Validation

This slice is ready when repeated batch-loop and failure-handling orchestration live behind their own `rag` seam and ingestion/embedding/indexing command behavior remains unchanged.

## Status

- Completed on `2026-06-14`.
- Checks passed:
  - `./.venv/bin/python -m ruff check rag/ingestion.py rag/ingestion_batch.py rag/ingestion_batch_runtime.py tests/test_ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py specs/2026-06-15-rag-batch-command-loop-and-failure-handling-seam-extraction --ignore E501`
  - `./.venv/bin/python -m pytest -q tests/test_ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py`

## Planned Checks

1. `./.venv/bin/python -m pytest -q tests/test_ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/ingestion_batch.py rag/ingestion_batch_runtime.py tests/test_ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py specs/2026-06-15-rag-batch-command-loop-and-failure-handling-seam-extraction --ignore E501`

## Expected Evidence

- `fail_fast=true` still halts on the first failed artifact for ingestion, embeddings, and indexing;
- `fail_fast=false` still records failures and continues processing;
- command-specific fallback manifest records still carry the same fields and error messages;
- no-match and missing-directory exits remain unchanged;
- `rag.ingestion.py` remains the top-level CLI dispatch surface.
