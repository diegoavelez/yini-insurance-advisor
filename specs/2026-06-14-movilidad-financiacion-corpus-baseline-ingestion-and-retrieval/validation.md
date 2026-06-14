# Validation

This slice is ready when the `financiación` cohort has completed the baseline
ingestion → embeddings → indexing → first retrieval loop with cohort-local
commands and documented evidence.

## Acceptance Checks

- The spec bundle exists.
- The cohort-only ingestion command is documented.
- The cohort-only embeddings command is documented.
- The cohort-only indexing command is documented.
- At least one financing-style retrieval check is documented.
- The roadmap records this as the next operational transversal cohort.

## Cohort Commands

### 1. Ingest only this cohort

- `make batch-ingest BATCH_VENV=./.venv BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/TRANSVERSALES/*financiacion*.pdf' BATCH_OVERWRITE=false`

### 2. Generate embeddings only for this cohort

- `make batch-embeddings BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_MANIFEST=data/processed/embedding-manifest.jsonl BATCH_CHUNK_GLOB='movilidad__transversales__*financiacion*.chunks.json' BATCH_OVERWRITE=true`

### 3. Index only this cohort

- `make batch-index BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_INDEX_MANIFEST=data/processed/qdrant-indexing-manifest.jsonl BATCH_EMBEDDING_GLOB='movilidad__transversales__*financiacion*.embeddings.json'`

### 4. First retrieval checks

- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'cómo funciona la financiación de pólizas en movilidad' --product movilidad --document-type guide --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué opciones de financiación hay para la póliza' --product movilidad --document-type guide --top-k 5`

## Expected Outcome

- The financing document is ingested and retrievable without broadening the
  rest of `MOVILIDAD/TRANSVERSALES`.
- Real retrieval evidence determines whether the next slice is needed.

## Execution Notes

- `make batch-ingest BATCH_VENV=./.venv BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/TRANSVERSALES/*financiacion*.pdf' BATCH_OVERWRITE=false` passed locally.
- `make batch-embeddings BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_MANIFEST=data/processed/embedding-manifest.jsonl BATCH_CHUNK_GLOB='movilidad__transversales__*financiacion*.chunks.json' BATCH_OVERWRITE=true` passed locally.
- `make batch-index BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_INDEX_MANIFEST=data/processed/qdrant-indexing-manifest.jsonl BATCH_EMBEDDING_GLOB='movilidad__transversales__*financiacion*.embeddings.json'` passed locally.
- Artifact inspection then showed:
  - `document_name = instructivo financiacion de polizas v1`
  - `chunk_count = 1`
  - cleaned markdown content collapsed to `sura`
- Live retrieval for both financing-oriented queries returned unrelated
  `PROPUESTA DE VALOR MOVILIDAD` chunks, so the follow-on issue is extraction
  readiness rather than query-family scoping.
