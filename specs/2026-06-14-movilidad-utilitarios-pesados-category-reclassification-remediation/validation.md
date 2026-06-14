# Validation

This slice is ready when the canonical `UTILITARIO Y PESADOS` classification is
represented consistently in code, tests, and operator runbooks.

## Automated checks

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'utilitarios or transversales_overlay'`
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'utilitarios'`
- `./.venv/bin/python -m pytest tests/test_query_scope.py -q`

## Canonical operator migration commands

Reingest only the dedicated category path:

- `make batch-ingest BATCH_VENV=./.venv BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/UTILITARIO Y PESADOS/*.pdf' BATCH_OVERWRITE=false`

Generate embeddings only for the canonical category artifacts:

- `make batch-embeddings BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_MANIFEST=data/processed/embedding-manifest.jsonl BATCH_CHUNK_GLOB='movilidad__utilitario-y-pesados__*.chunks.json' BATCH_OVERWRITE=true`

Index only the canonical category embeddings:

- `make batch-index BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_INDEX_MANIFEST=data/processed/qdrant-indexing-manifest.jsonl BATCH_EMBEDDING_GLOB='movilidad__utilitario-y-pesados__*.embeddings.json'`

Run one guide and one policy retrieval check against the corrected product:

- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué beneficios o asistencias tienen los utilitarios y pesados' --product 'utilitarios y pesados' --document-type guide --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué cubre el plan de utilitarios y pesados' --product 'utilitarios y pesados' --document-type policy --top-k 5`

## Expected evidence

- overlay-backed ingestion persists the two PDFs under
  `movilidad__utilitario-y-pesados__...`;
- retrieval tests no longer reference
  `MOVILIDAD/TRANSVERSALES/*utilitarios*y*pesados*`;
- roadmap notes state that the prior transversal assumption was corrected.
