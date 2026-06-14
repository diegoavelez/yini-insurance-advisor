# Validation

Executed checks for this slice:

1. `make -n batch-ingest BATCH_GLOB='MOVILIDAD/TRANSVERSALES/*choque simple*.pdf'`
2. `make -n batch-embeddings BATCH_CHUNK_GLOB='movilidad__transversales__*choque-simple*.chunks.json'`
3. `make -n batch-index BATCH_EMBEDDING_GLOB='movilidad__transversales__*choque-simple*.embeddings.json'`

Observed outcome:

- The operator workflow can now target only the `choque simple` transversal
  raw PDFs without editing committed command templates.
- The same narrow cohort can be propagated through embeddings generation and
  Qdrant indexing with matching artifact globs.
