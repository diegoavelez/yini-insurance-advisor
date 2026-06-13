# Validation

This slice is ready when `MOVILIDAD/BICICLETAS Y PATINETAS` is ingested into the current RAG baseline and can answer real retrieval queries under the existing `movilidad` taxonomy.

## Acceptance Checks

- The spec bundle exists.
- `movilidad` aliases cover bicycles and scooters.
- `pv` can persist as `guide` when appropriate.
- The three source PDFs are ingested.
- Embeddings are generated and indexed.
- Real retrieval queries return category-relevant chunks.
- The roadmap records the slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
- `./.venv/bin/python -m ruff check tests/test_ingestion.py`
- `./.venv/bin/python -m rag.ingestion ingest-pdfs --input-dir data/raw --markdown-dir data/markdown --processed-dir data/processed --manifest-path data/processed/ingestion-manifest.jsonl --glob '*bicis*pdf' --overwrite false --fail-fast true`
- `./.venv/bin/python -m rag.ingestion generate-embeddings --chunk-dir data/processed/chunks --embedding-dir data/processed/embeddings --manifest-path data/processed/embedding-manifest.jsonl --glob 'movilidad__bicicletas-y-patinetas__*.chunks.json' --overwrite false --fail-fast true`
- `./.venv/bin/python -m rag.ingestion index-embeddings --embedding-dir data/processed/embeddings --manifest-path data/processed/qdrant-indexing-manifest.jsonl --glob 'movilidad__bicicletas-y-patinetas__*.embeddings.json' --fail-fast true`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el seguro para bicicleta?' --top-k 5 --product movilidad`
