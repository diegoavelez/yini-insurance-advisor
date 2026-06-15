# Validation

This slice is ready when markdown/chunk normalization logic lives behind its own
`rag` seam and validated corpus behavior remains unchanged.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_ingestion.py tests/test_document_canonicalization.py tests/test_grounded_answer_generation.py tests/test_retrieval.py -q -k 'muevete or suscripcion or choque_simple or pv or deducti or comparison or document_canonicalization or arl and remuneration'`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/arl_remuneration.py rag/document_canonicalization.py rag/markdown_chunk_normalization.py tests/test_document_canonicalization.py tests/test_grounded_answer_generation.py`
3. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre Muévete Libre?' --top-k 5 --product 'muevete libre'`
4. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`

## Expected Evidence

- known-document normalization still yields the same semantic headings and
  `section_path` lineage for validated corpora;
- PV/comparison/deductible/circular block normalization behavior stays stable;
- live `Muévete Libre` and ARL answer queries remain supported with the current
  evidence quality.
