# Validation

Executed checks in this harness:

1. `make batch-embeddings BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_MANIFEST=data/processed/embedding-manifest.jsonl BATCH_CHUNK_GLOB='movilidad__transversales__pv-*.chunks.json' BATCH_OVERWRITE=true`
2. `make batch-index BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_INDEX_MANIFEST=data/processed/qdrant-indexing-manifest.jsonl BATCH_EMBEDDING_GLOB='movilidad__transversales__pv-*.embeddings.json'`

Observed outcome:

- `PV` embeddings now generate successfully from the latest chunk artifacts.
- Successful local embedding artifacts:
  - `data/processed/embeddings/movilidad__transversales__pv-planes-movilidad-v1.embeddings.json`
  - `data/processed/embeddings/movilidad__transversales__pv-portafolio-movilidad-v2.embeddings.json`
- The embedding manifest now includes succeeded records for both `PV` sources.
- Qdrant indexing does not fail because of code or credentials in this harness;
  it fails because sandboxed network resolution to the external Qdrant host is
  blocked here (`[Errno 8] nodename nor servname provided, or not known`).

Operational handoff:

- Run the indexing command in a terminal/session with outbound network access:
  `make batch-index BATCH_PYTHON=./.venv/bin/python BATCH_PROCESSED_DIR=data/processed BATCH_INDEX_MANIFEST=data/processed/qdrant-indexing-manifest.jsonl BATCH_EMBEDDING_GLOB='movilidad__transversales__pv-*.embeddings.json'`
- Then verify retrieval with one live query, for example:
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué beneficios incluye la propuesta de valor de movilidad' --product movilidad --document-type guide --top-k 5`

Conclusion in this harness:

- Embeddings: `GO`
- Qdrant indexing: `BLOCKED BY HARNESS NETWORK POLICY`
- Retrieval verification: `PENDING INDEXING RUN`
