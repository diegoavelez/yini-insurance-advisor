# Validation

This slice is ready when the ARL remuneration-policy flow behaves exactly as
before while `rag/ingestion.py` delegates that domain to a dedicated module.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_grounded_answer_generation.py tests/test_retrieval.py -q -k 'arl and remuneration'`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/arl_remuneration.py tests/test_grounded_answer_generation.py tests/test_retrieval.py`
3. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`

## Expected Evidence

- broad ARL remuneration retrieval still leads with the intended direct policy
  sections;
- explicit percentage/table queries still preserve the existing table-first
  behavior;
- broad remuneration grounded answers still keep compact direct-support
  citations with `confidence=high`.
