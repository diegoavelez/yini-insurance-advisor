# Validation

Planned checks for this slice:

1. `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
3. Rebuild the `movilidad__transversales__como-tomar-fotos-choque-simple-v2`
   artifacts.
4. `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo tomar fotos en un choque simple?' --top-k 5`
