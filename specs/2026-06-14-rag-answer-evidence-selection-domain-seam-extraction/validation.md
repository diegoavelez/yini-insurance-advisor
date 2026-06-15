# Validation

This slice is ready when domain-specific evidence-selection helpers live behind
their own `rag` seam and validated retrieval/answer behavior remains unchanged.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_retrieval.py tests/test_grounded_answer_generation.py tests/test_observability.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/evidence_selection.py tests/test_retrieval.py tests/test_grounded_answer_generation.py tests/test_observability.py`
3. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`

## Expected Evidence

- specialized reranking and candidate-pool sizing tests still pass;
- movilidad suscripción answer-evidence narrowing still passes;
- ARL guide/RUI/remuneration citation narrowing still passes;
- a live grounded-answer query still succeeds against the current runtime.
