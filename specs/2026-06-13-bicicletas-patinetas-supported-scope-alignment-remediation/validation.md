# Validation

- Deterministic supported-scope classification admits representative Spanish
  bicycle/scooter insurance queries from the current corpus.
- Existing unsupported non-insurance Spanish queries remain unsupported.
- A real `answer-query` validation for the category no longer returns an
  `unsupported_scope_refusal`.

## Suggested Checks

- `./.venv/bin/python -m pytest tests/test_query_scope.py tests/test_ingestion.py -q`
- `./.venv/bin/python -m ruff check core/query_scope.py tests/test_query_scope.py`
- `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre el seguro para bicicletas y patinetas?' --product movilidad --top-k 5`
