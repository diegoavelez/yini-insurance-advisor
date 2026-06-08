# Validation

## Status

- Completed on `2026-06-08`.
- Checks passed:
  - `./.venv/bin/python -m ruff check core/config.py rag/ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
  - `./.venv/bin/python -m pytest tests/test_embedding_generation.py tests/test_qdrant_indexing.py tests/test_retrieval.py -q`

## Required Checks

- `./.venv/bin/python -m ruff check core/config.py rag/ingestion.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
- `./.venv/bin/python -m pytest tests/test_embedding_generation.py tests/test_qdrant_indexing.py tests/test_retrieval.py`

## Required Scenarios

- The default embedding model is multilingual.
- Embedding generation still uses the existing `sentence-transformers` seam.
- Retrieval tests still pass with the multilingual default configured.
- The slice remains scoped away from query-scope and guardrail logic.

## Merge Readiness

This spec is ready when the retrieval-alignment slice is decision-complete for:

- multilingual default embeddings;
- stable preservation of the current provider/runtime seam;
- no drift into query-scope, guardrail, or evaluation changes.
