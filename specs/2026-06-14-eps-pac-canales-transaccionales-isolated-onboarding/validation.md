# Validation

This slice is ready when the final PAC transactional/support PDF is onboarded
and PAC category onboarding is complete for the current roadmap scope.

## Automated checks

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'pac and canales_transaccionales'`
- `./.venv/bin/python -m pytest tests/test_query_scope.py -q -k 'pac_canales_transaccionales'`

## Canonical operator sequence

- Warm-up:
  - `make batch-warmup BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_SAMPLE_PDF="data/raw/EPS/PLAN COMPLEMENTARIO PAC/informacion canales transaccionales y apoyo v1.pdf"`
- Cohort ingestion:
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/informacion canales transaccionales y apoyo v1.pdf' BATCH_OVERWRITE=false`
- Cohort embeddings:
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_CHUNK_GLOB='eps__plan-complementario-pac__informacion-canales-transaccionales-y-apoyo-v1.chunks.json' BATCH_OVERWRITE=false`
- Cohort indexing:
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_GLOB='eps__plan-complementario-pac__informacion-canales-transaccionales-y-apoyo-v1.embeddings.json'`
- Retrieval verification:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué canales transaccionales y de apoyo tiene el plan complementario PAC?' --product 'pac' --top-k 5`

## Deferred PAC groups

- Unsupported `.docx`:
  - `propuesta renovacion contratos colectivos 60 mas v1.docx`
  - `propuesta renovacion contratos colectivos tradicionales v1.docx`

## Validation evidence

- `batch-warmup` succeeded for `informacion canales transaccionales y apoyo v1.pdf`.
- `informacion canales transaccionales y apoyo v1.pdf` ingested successfully
  with `BATCH_OVERWRITE=false`.
- The resulting processed metadata confirmed the intended PAC operational/support
  posture:
  - `eps__plan-complementario-pac__informacion-canales-transaccionales-y-apoyo-v1`
    resolved to `document_name="informacion canales transaccionales y apoyo v1"`,
    `product="pac"`, `document_type="guide"`.
- The document chunk family embedded successfully:
  - `eps__plan-complementario-pac__informacion-canales-transaccionales-y-apoyo-v1.chunks.json`
- The embedding family indexed successfully into Qdrant Cloud:
  - `eps__plan-complementario-pac__informacion-canales-transaccionales-y-apoyo-v1.embeddings.json`
- Initial live retrieval for `¿Qué canales transaccionales y de apoyo tiene el
  plan complementario PAC?` still preferred `tips medios de pago v3.pdf`
  before the new family was indexed.
- Final live retrieval after onboarding succeeded without additional
  term-equivalence routing:
  - `¿Qué canales transaccionales y de apoyo tiene el plan complementario PAC?`
    retrieved `informacion canales transaccionales y apoyo v1` first.
  - `¿Qué apoyo comercial y canales de trámite tiene el PAC?` also retrieved
    `informacion canales transaccionales y apoyo v1` first.
- No narrow routing rule was added in this slice because the indexed document
  already ranks first for the validated operational intents.
