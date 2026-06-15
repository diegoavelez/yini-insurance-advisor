# Validation

This slice is ready when Qdrant payload/filter/bootstrap logic lives behind its
own `rag` seam and validated retrieval/indexing behavior remains unchanged.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_retrieval.py tests/test_grounded_answer_generation.py tests/test_ingestion.py -q -k 'qdrant or metadata filter or indexing or source_pdf_id or arl and remuneration'`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/qdrant_store.py tests/test_retrieval.py tests/test_grounded_answer_generation.py`
3. `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre Muévete Libre?' --product 'muevete libre' --top-k 5`
4. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`

## Expected Evidence

- deterministic point ids and payload fields are preserved;
- retrieval filters still map to the same Qdrant payload keys;
- collection bootstrap and payload-index setup stay compatible with the current
  client/runtime surface;
- live retrieval and grounded-answer flows still succeed against the existing
  Qdrant collection.
