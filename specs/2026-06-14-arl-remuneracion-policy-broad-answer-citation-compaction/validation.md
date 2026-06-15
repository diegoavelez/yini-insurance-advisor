# Validation

This slice is ready when broad ARL remuneration overview answers keep their
current supported behavior while exposing a shorter, direct-support evidence
trail.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_grounded_answer_generation.py tests/test_retrieval.py -q -k 'arl and remuneration'`
2. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_grounded_answer_generation.py tests/test_retrieval.py`
3. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`

## Expected Evidence

- broad ARL remuneration overview answers keep `confidence=high`;
- `documentary_basis` and `citations` exclude lateral policy chunks such as
  `Política de designación de intermediarios...` when direct overview support is
  already sufficient;
- direct support chunks such as overview, appetite/table, and change of
  intermediary remain available when present.
