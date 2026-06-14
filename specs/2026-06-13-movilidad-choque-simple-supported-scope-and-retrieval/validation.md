# Validation

Planned checks for this slice:

1. `./.venv/bin/python -m pytest tests/test_query_scope.py tests/test_retrieval.py -q`
2. `./.venv/bin/python -m ruff check core/query_scope.py tests/test_query_scope.py tests/test_retrieval.py`
3. `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué debo hacer en un choque simple?' --top-k 5`
