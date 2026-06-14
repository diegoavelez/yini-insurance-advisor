# Validation

This slice is ready when the `MOVILIDAD/VIAJES` category is operational through
the canonical onboarding path.

## Automated checks

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'viajes'`
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'viajes'`
- `./.venv/bin/python -m pytest tests/test_query_scope.py -q -k 'viajes'`

## Canonical operator commands

- `make batch-ingest BATCH_VENV=./.venv BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/VIAJES/*.pdf' BATCH_OVERWRITE=false`
- `make batch-embeddings BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_MANIFEST=data/processed/embedding-manifest.jsonl BATCH_CHUNK_GLOB='movilidad__viajes__*.chunks.json' BATCH_OVERWRITE=true`
- `make batch-index BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_INDEX_MANIFEST=data/processed/qdrant-indexing-manifest.jsonl BATCH_EMBEDDING_GLOB='movilidad__viajes__*.embeddings.json'`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué beneficios incluye el seguro de viajes' --product 'viajes' --document-type guide --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué cubre el clausulado de viaje internacional' --product 'viajes' --document-type policy --top-k 5`
