# Validation

This slice is ready when table-like comparison content can be normalized into semantically richer text before chunking.

## Acceptance Checks

- The spec bundle exists.
- Comparison-table blocks can normalize into plan-oriented statements.
- Non-table content remains unchanged.
- Focused ingestion tests pass.
- The AUTOS comparative document can be re-embedded and reindexed.
- The roadmap records the slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- `./.venv/bin/python -m rag.ingestion generate-embeddings --chunk-dir data/processed/chunks --embedding-dir data/processed/embeddings --manifest-path data/processed/embedding-manifest.jsonl --glob 'movilidad__autos__diferenciales-planes-autos.chunks.json' --overwrite true --fail-fast true`
- `./.venv/bin/python -m rag.ingestion index-embeddings --embedding-dir data/processed/embeddings --manifest-path data/processed/qdrant-indexing-manifest.jsonl --glob 'movilidad__autos__diferenciales-planes-autos.embeddings.json' --fail-fast true`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué diferencias hay entre el plan básico y los otros planes de autos?' --top-k 12 --product auto`
