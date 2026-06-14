# Validation

Executed checks for this slice:

1. `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
2. `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
3. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
4. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
5. `./.venv/bin/python -m rag.ingestion generate-embeddings --chunk-dir data/processed/chunks --embedding-dir data/processed/embeddings --manifest-path data/processed/embedding-manifest.jsonl --glob 'movilidad__transversales__circular-choque-simple.chunks.json' --overwrite true --fail-fast true`
6. `./.venv/bin/python -m rag.ingestion index-embeddings --embedding-dir data/processed/embeddings --manifest-path data/processed/qdrant-indexing-manifest.jsonl --glob 'movilidad__transversales__circular-choque-simple.embeddings.json' --fail-fast true`
7. `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué debo hacer en un choque simple?' --top-k 5`

Observed outcome:

- Ingestion now strips circular-specific boilerplate and promotes semantic
  sections such as `ASUNTO CHOQUE SIMPLE` and
  `INSTRUCCIONES OPERATIVAS CHOQUE SIMPLE`.
- Live retrieval no longer leaks `auto`/`moto` policy chunks ahead of the
  transversal guide when `choque simple` rules normalize filters to
  `product=movilidad` and `document_type=guide`.
- Live top-5 retrieval now stays entirely inside
  `MOVILIDAD/TRANSVERSALES/circular choque simple.pdf`, with operational
  evidence chunks present in the leading results.
