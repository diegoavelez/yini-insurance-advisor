# Validation

Planned checks for this slice:

1. `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
3. `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el SOAT?' --top-k 5 --product soat`
4. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre el SOAT?' --top-k 5 --product soat`
