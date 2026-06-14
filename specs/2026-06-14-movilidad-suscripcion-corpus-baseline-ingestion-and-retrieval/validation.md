# Validation

This slice is ready when the `suscripción` cohort has completed the baseline
ingestion → embeddings → indexing → first retrieval loop with cohort-local
commands and documented evidence.

## Acceptance Checks

- The spec bundle exists.
- The cohort-only ingestion command is documented.
- The cohort-only embeddings command is documented.
- The cohort-only indexing command is documented.
- At least one suscripción-style retrieval check is documented.
- The roadmap remains consistent with this as the next operational transversal
  cohort.

## Cohort Commands

### 1. Ingest only this cohort

- `make batch-ingest BATCH_VENV=./.venv BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/TRANSVERSALES/*suscripcion*.pdf' BATCH_OVERWRITE=false BATCH_DOCLING_TIMEOUT=120`

### 2. Generate embeddings only for this cohort

- `make batch-embeddings BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_MANIFEST=data/processed/embedding-manifest.jsonl BATCH_CHUNK_GLOB='movilidad__transversales__*suscripcion*.chunks.json' BATCH_OVERWRITE=true`

### 3. Index only this cohort

- `make batch-index BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_INDEX_MANIFEST=data/processed/qdrant-indexing-manifest.jsonl BATCH_EMBEDDING_GLOB='movilidad__transversales__*suscripcion*.embeddings.json'`

### 4. First retrieval checks

- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'cuáles son las políticas de suscripción de movilidad' --product movilidad --document-type policy --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué reglas de suscripción aplican en movilidad' --product movilidad --document-type policy --top-k 5`

## Expected Outcome

- The suscripción document is ingested and retrievable without broadening the
  rest of `MOVILIDAD/TRANSVERSALES`.
- Real retrieval evidence determines whether the next corrective slice is
  needed.

## Execution Notes

- `make batch-ingest BATCH_VENV=./.venv BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/TRANSVERSALES/*suscripcion*.pdf' BATCH_OVERWRITE=false BATCH_DOCLING_TIMEOUT=120` passed locally.
- The original baseline command with `BATCH_DOCLING_TIMEOUT=1800` did not fail,
  but remained inside Docling conversion for more than 13 minutes on the
  64-page source PDF without producing artifacts, so the validated cohort run
  used a lower operational timeout to trigger the existing PDFium fallback.
- `make batch-embeddings BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_MANIFEST=data/processed/embedding-manifest.jsonl BATCH_CHUNK_GLOB='movilidad__transversales__*suscripcion*.chunks.json' BATCH_OVERWRITE=true` passed locally.
- `make batch-index BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_INDEX_MANIFEST=data/processed/qdrant-indexing-manifest.jsonl BATCH_EMBEDDING_GLOB='movilidad__transversales__*suscripcion*.embeddings.json'` passed locally.
- Persisted artifact evidence now shows:
  - `document_name = politicas de suscripcion de movilidad`
  - `document_type = policy`
  - `product = movilidad`
  - `chunk_count = 143`
- Live retrieval for:
  - `cuáles son las políticas de suscripción de movilidad`
  - `qué reglas de suscripción aplican en movilidad`
  stayed inside the suscripción document family, so there is no immediate
  cross-document leakage gap.
- However, the retrieved chunks still expose weak fallback structure such as
  `Page 9`, `Page 43`, and short residual fragments like `iarios`, which means
  the next narrow issue is extraction/section-structure quality rather than
  document-family alignment.
