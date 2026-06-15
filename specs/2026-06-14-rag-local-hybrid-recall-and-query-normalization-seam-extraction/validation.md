# Validation

This slice is ready when local hybrid-recall and retrieval-query normalization
helpers live behind their own `rag` seam and validated retrieval behavior
remains unchanged.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_retrieval.py tests/test_observability.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/local_hybrid_recall.py tests/test_retrieval.py tests/test_observability.py`
3. `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué beneficios incluye la propuesta de valor de movilidad' --product movilidad --document-type guide --top-k 5`

## Expected Evidence

- retrieval normalization and lexical enrichment tests still pass;
- local lexical fallback ordering still passes;
- applicability-dedup behavior still passes;
- a live retrieval query still succeeds against the current runtime.
