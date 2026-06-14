# Validation

This slice is ready when the `utilitarios y pesados` cohort has completed the
baseline ingestion → embeddings → indexing → first retrieval loop with
cohort-local commands and documented evidence.

## Acceptance Checks

- The spec bundle exists.
- The cohort-only ingestion command is documented.
- The cohort-only embeddings command is documented.
- The cohort-only indexing command is documented.
- At least one guide-style and one policy-style retrieval check are documented.
- The roadmap records this as the next operational cohort.

## Cohort Commands

### 1. Ingest only this cohort

- `make batch-ingest BATCH_VENV=./.venv BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/TRANSVERSALES/*utilitarios*y*pesados*.pdf' BATCH_OVERWRITE=false`

### 2. Generate embeddings only for this cohort

- `make batch-embeddings BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_MANIFEST=data/processed/embedding-manifest.jsonl BATCH_CHUNK_GLOB='movilidad__transversales__*utilitarios-y-pesados*.chunks.json' BATCH_OVERWRITE=true`

### 3. Index only this cohort

- `make batch-index BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_INDEX_MANIFEST=data/processed/qdrant-indexing-manifest.jsonl BATCH_EMBEDDING_GLOB='movilidad__transversales__*utilitarios-y-pesados*.embeddings.json'`

### 4. First retrieval checks

- Guide-oriented:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué beneficios o asistencias tienen los utilitarios y pesados' --product movilidad --document-type guide --top-k 5`
- Policy-oriented:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué cubre el plan de utilitarios y pesados' --product movilidad --document-type policy --top-k 5`

## Expected Outcome

- The two-document cohort is ingested and retrievable without broadening the
  rest of `MOVILIDAD/TRANSVERSALES`.
- Real retrieval evidence determines whether the next slice is needed.
