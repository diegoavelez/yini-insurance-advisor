# Validation

This slice is ready when the general PAC asegurabilidad policy is onboarded and
general PAC asegurabilidad queries no longer drift into the `PAC 60+` family.

## Automated checks

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'pac and policy_follow_on'`
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'pac_asegurabilidad_document_name or general_pac_asegurabilidad_document_name'`

## Canonical operator sequence

- Warm-up:
  - `make batch-warmup BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_SAMPLE_PDF="data/raw/EPS/PLAN COMPLEMENTARIO PAC/politicas asegurabilidad pac v16.pdf"`
- Cohort ingestion:
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/politicas asegurabilidad pac v16.pdf' BATCH_OVERWRITE=false`
- Cohort embeddings:
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_CHUNK_GLOB='eps__plan-complementario-pac__politicas-asegurabilidad-pac-v16.chunks.json' BATCH_OVERWRITE=false`
- Cohort indexing:
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_GLOB='eps__plan-complementario-pac__politicas-asegurabilidad-pac-v16.embeddings.json'`
- Retrieval verification:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product 'pac' --document-type policy --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué condiciones de asegurabilidad tiene el plan complementario PAC?' --product 'pac' --document-type policy --top-k 5`

## Deferred PAC groups

- Large isolated PDFs:
  - `informacion canales transaccionales y apoyo v1.pdf`
  - `clausulado pac tradicional sura v1.pdf`
- Unsupported `.docx`:
  - `propuesta renovacion contratos colectivos 60 mas v1.docx`
  - `propuesta renovacion contratos colectivos tradicionales v1.docx`

## Validation evidence

- Before onboarding `v16`, both of the following queries incorrectly returned
  only `eps__plan-complementario-pac__politicas-asegurabilidad-pac-60-mas`
  chunks because the existing PAC `60+` asegurabilidad rule captured any
  generic `pac` asegurabilidad query:
  - `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?`
  - `¿Qué condiciones de asegurabilidad tiene el plan complementario PAC?`
- `batch-warmup` succeeded for `politicas asegurabilidad pac v16.pdf`.
- `politicas asegurabilidad pac v16.pdf` ingested successfully with
  `BATCH_OVERWRITE=false`.
- The resulting processed metadata confirmed the intended general PAC policy
  posture:
  - `eps__plan-complementario-pac__politicas-asegurabilidad-pac-v16`
    resolved to `document_name="Políticas Plan Complementario EPS SURA"`,
    `document_version="ABRIL"`, `product="pac"`, `document_type="policy"`.
- The `v16` chunk family embedded successfully:
  - `eps__plan-complementario-pac__politicas-asegurabilidad-pac-v16.chunks.json`
- The `v16` embedding family indexed successfully into Qdrant Cloud:
  - `eps__plan-complementario-pac__politicas-asegurabilidad-pac-v16.embeddings.json`
- PAC term-equivalence routing was narrowed and extended as follows:
  - `PAC 60+` asegurabilidad now requires explicit `60 mas` wording plus
    `pac` or `plan complementario`
  - generic `asegurabilidad` plus `pac` or `plan complementario` now pins to
    `document_name="Políticas Plan Complementario EPS SURA"`
- Final live retrieval after onboarding and routing correction succeeded:
  - `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` still retrieved
    `Plan Complementario 60 más` first
  - `¿Qué condiciones de asegurabilidad tiene el plan complementario PAC?`
    now retrieved `Políticas Plan Complementario EPS SURA` first
