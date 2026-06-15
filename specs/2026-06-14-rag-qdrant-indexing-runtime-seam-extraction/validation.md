# Validation

This slice is ready when the remaining Qdrant indexing runtime helpers live
behind `rag/qdrant_store.py` and the validated indexing behavior remains
unchanged.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_qdrant_indexing.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/qdrant_store.py tests/test_qdrant_indexing.py`
3. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`

## Expected Evidence

- retry/backoff indexing tests still pass;
- prune and smoke validation paths still pass;
- live retrieval-backed answer generation still succeeds against the current
  Qdrant collection after the seam extension.
