# Validation

Planned checks for this slice:

1. `./.venv/bin/python -m pytest tests/test_query_scope.py tests/test_ingestion.py -q`
2. `./.venv/bin/python -m ruff check core/query_scope.py tests/test_query_scope.py tests/test_ingestion.py rag/ingestion.py`
3. `python -m rag.ingestion ingest-pdfs ... --glob 'MOVILIDAD/MUEVETE LIBRE/*.pdf'`
4. `python -m rag.ingestion generate-embeddings ... --glob 'movilidad__muevete-libre__*.chunks.json'`
5. `python -m rag.ingestion index-embeddings ... --glob 'movilidad__muevete-libre__*.embeddings.json'`
6. `python -m rag.ingestion retrieve-chunks --query '¿Qué cubre Muévete Libre?' --top-k 5 --product 'muevete libre'`
