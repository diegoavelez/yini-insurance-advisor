# Validation

This slice is ready when fragmented structured sections can produce denser grouped blocks without changing the chunk contract.

## Acceptance Checks

- The spec bundle exists.
- Same-section aggregation can merge more than one short adjacent block.
- Heading/clause anchoring still works.
- Focused chunking tests pass.
- The AUTOS comparative document can be regenerated and reindexed under the new chunking logic.
- The roadmap records the slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- `./.venv/bin/python -m rag.ingestion generate-embeddings --chunk-dir data/processed/chunks --embedding-dir data/processed/embeddings --manifest-path data/processed/embedding-manifest.jsonl --glob 'movilidad__autos__diferenciales-planes-autos.chunks.json' --overwrite true --fail-fast true`
- `./.venv/bin/python -m rag.ingestion index-embeddings --embedding-dir data/processed/embeddings --manifest-path data/processed/qdrant-indexing-manifest.jsonl --glob 'movilidad__autos__diferenciales-planes-autos.embeddings.json' --fail-fast true`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué diferencias hay entre el plan básico y los otros planes de autos?' --top-k 12 --product auto`
