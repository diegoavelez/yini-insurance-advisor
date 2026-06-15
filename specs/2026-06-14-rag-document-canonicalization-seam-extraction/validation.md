# Validation

This slice is ready when document canonicalization logic lives behind its own
`rag` seam and behavior stays unchanged for the validated paths.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_document_canonicalization.py tests/test_grounded_answer_generation.py tests/test_retrieval.py -q -k 'document_canonicalization or arl and remuneration'`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/arl_remuneration.py rag/document_canonicalization.py tests/test_document_canonicalization.py tests/test_grounded_answer_generation.py`
3. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`

## Expected Evidence

- document metadata extraction still prefers safe markdown headings and version
  lines when available;
- nested raw paths still derive stable collision-safe `source_pdf_id` values and
  deterministic artifact paths;
- overlay-first product/document-type resolution remains unchanged;
- the live ARL remuneration answer remains supported with high confidence and
  compact direct-support citations.
