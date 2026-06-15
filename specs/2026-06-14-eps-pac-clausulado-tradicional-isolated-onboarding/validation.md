# Validation

This slice is ready when the traditional PAC clausulado is onboarded and
generic PAC coverage queries no longer drift into the `PAC 60+` clausulado
family.

## Automated checks

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'pac and clausulado_tradicional'`
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'pac_clausulado_document_name or general_pac_clausulado_document_name or explicit_general_pac_clausulado_document_name'`

## Canonical operator sequence

- Warm-up:
  - `make batch-warmup BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_SAMPLE_PDF="data/raw/EPS/PLAN COMPLEMENTARIO PAC/clausulado pac tradicional sura v1.pdf"`
- Cohort ingestion:
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/clausulado pac tradicional sura v1.pdf' BATCH_OVERWRITE=false`
- Cohort embeddings:
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_CHUNK_GLOB='eps__plan-complementario-pac__clausulado-pac-tradicional-sura-v1.chunks.json' BATCH_OVERWRITE=false`
- Cohort indexing:
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_GLOB='eps__plan-complementario-pac__clausulado-pac-tradicional-sura-v1.embeddings.json'`
- Retrieval verification:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el PAC 60 Más?' --product 'pac' --document-type policy --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el plan complementario PAC?' --product 'pac' --document-type policy --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el clausulado del plan complementario PAC?' --product 'pac' --document-type policy --top-k 5`

## Deferred PAC groups

- Large isolated PDFs:
  - `informacion canales transaccionales y apoyo v1.pdf`
- Unsupported `.docx`:
  - `propuesta renovacion contratos colectivos 60 mas v1.docx`
  - `propuesta renovacion contratos colectivos tradicionales v1.docx`

## Validation evidence

- Before onboarding the traditional clausulado, both of the following queries
  incorrectly returned only `eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1`
  chunks because the existing broad PAC clausulado rules still pointed to the
  `PAC 60+` family:
  - `¿Qué cubre el plan complementario PAC?`
  - `¿Qué cubre el clausulado del plan complementario PAC?`
- `batch-warmup` succeeded for `clausulado pac tradicional sura v1.pdf`.
- `clausulado pac tradicional sura v1.pdf` ingested successfully with
  `BATCH_OVERWRITE=false`.
- The resulting processed metadata confirmed the intended traditional PAC policy
  posture:
  - `eps__plan-complementario-pac__clausulado-pac-tradicional-sura-v1`
    resolved to `document_name="OBLIGACIONES DE EPS SURA"`,
    `product="pac"`, `document_type="policy"`.
- The traditional clausulado chunk family embedded successfully:
  - `eps__plan-complementario-pac__clausulado-pac-tradicional-sura-v1.chunks.json`
- The traditional clausulado embedding family indexed successfully into Qdrant
  Cloud:
  - `eps__plan-complementario-pac__clausulado-pac-tradicional-sura-v1.embeddings.json`
- PAC clausulado routing was narrowed and extended as follows:
  - `PAC 60+` clausulado now requires explicit `60 mas` wording plus
    coverage/clausulado intent terms;
  - generic PAC coverage/clausulado queries now pin to
    `document_name="OBLIGACIONES DE EPS SURA"`.
- Final live retrieval after onboarding and routing correction succeeded:
  - `¿Qué cubre el PAC 60 Más?` still retrieved `Es tiempo devIvIr mas historias.` first;
  - `¿Qué cubre el plan complementario PAC?` now retrieved
    `OBLIGACIONES DE EPS SURA` first;
  - `¿Qué cubre el clausulado del plan complementario PAC?` also retrieved
    `OBLIGACIONES DE EPS SURA` first.
