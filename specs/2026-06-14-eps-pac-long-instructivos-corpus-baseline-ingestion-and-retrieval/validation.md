# Validation

This slice is ready when the two long PAC instructivos are onboarded and
validated without broadening into the remaining PAC folder.

## Automated checks

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'pac and long_instructivos'`
- `./.venv/bin/python -m pytest tests/test_query_scope.py -q -k 'pac_long_instructivos or pac_operational_queries'`

## Canonical operator sequence

- Warm-up:
  - `make batch-warmup BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_SAMPLE_PDF="data/raw/EPS/PLAN COMPLEMENTARIO PAC/instructivo inclusion de asegurados cotizador v2.pdf"`
- Cohort ingestion, one PDF at a time:
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/instructivo inclusion de asegurados cotizador v2.pdf' BATCH_OVERWRITE=false`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/instructivo formularios web novedades pac v6.pdf' BATCH_OVERWRITE=false`
- Cohort embeddings, one chunk family at a time:
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDINGS_DIR=data/processed/embeddings BATCH_GLOB='eps__plan-complementario-pac__instructivo-inclusion-de-asegurados-cotizador-v2.chunks.json' BATCH_OVERWRITE=false`
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDINGS_DIR=data/processed/embeddings BATCH_GLOB='eps__plan-complementario-pac__instructivo-formularios-web-novedades-pac-v6.chunks.json' BATCH_OVERWRITE=false`
- Cohort indexing, one embedding family at a time:
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_EMBEDDINGS_DIR=data/processed/embeddings BATCH_MANIFEST_PATH=data/processed/qdrant-indexing-manifest.jsonl BATCH_GLOB='eps__plan-complementario-pac__instructivo-inclusion-de-asegurados-cotizador-v2.embeddings.json' BATCH_FAIL_FAST=true`
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_EMBEDDINGS_DIR=data/processed/embeddings BATCH_MANIFEST_PATH=data/processed/qdrant-indexing-manifest.jsonl BATCH_GLOB='eps__plan-complementario-pac__instructivo-formularios-web-novedades-pac-v6.embeddings.json' BATCH_FAIL_FAST=true`
- Retrieval verification:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo incluir asegurados en el cotizador PAC?' --product 'pac' --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo gestionar formularios web de novedades PAC?' --product 'pac' --top-k 5`

## Deferred PAC groups

- Future PAC policy cohort:
  - `politicas asegurabilidad pac v16.pdf`
- Large isolated PDFs:
  - `informacion canales transaccionales y apoyo v1.pdf`
  - `clausulado pac tradicional sura v1.pdf`
- Unsupported `.docx`:
  - `propuesta renovacion contratos colectivos 60 mas v1.docx`
  - `propuesta renovacion contratos colectivos tradicionales v1.docx`

## Validation evidence

- `batch-warmup` succeeded for `instructivo inclusion de asegurados cotizador v2.pdf`
  after an extended first-run Docling conversion window; the required assets are
  now cached locally.
- The two cohort PDFs ingested successfully with `BATCH_OVERWRITE=false`:
  - `instructivo inclusion de asegurados cotizador v2.pdf`
  - `instructivo formularios web novedades pac v6.pdf`
- The resulting processed metadata confirmed the intended PAC guide posture:
  - `eps__plan-complementario-pac__instructivo-inclusion-de-asegurados-cotizador-v2`
    resolved to `document_name="INCLUSIÓN DE ASEGURADOS A TRAVÉS DEL COTIZADOR CONTRATOS TRADICIONALES PLAN COMPLEMENTARIO"`,
    `document_version="02"`, `product="pac"`, `document_type="guide"`
  - `eps__plan-complementario-pac__instructivo-formularios-web-novedades-pac-v6`
    resolved to `document_name="SOLICITUD DE NOVEDADES AL CONTRATO DESDE FORMULARIOS WEB"`,
    `document_version="06"`, `product="pac"`, `document_type="guide"`
- The two chunk families embedded successfully:
  - `eps__plan-complementario-pac__instructivo-inclusion-de-asegurados-cotizador-v2.chunks.json`
  - `eps__plan-complementario-pac__instructivo-formularios-web-novedades-pac-v6.chunks.json`
- The two embedding families indexed successfully into Qdrant Cloud:
  - `eps__plan-complementario-pac__instructivo-inclusion-de-asegurados-cotizador-v2.embeddings.json`
  - `eps__plan-complementario-pac__instructivo-formularios-web-novedades-pac-v6.embeddings.json`
- Live retrieval succeeded without additional term-equivalence routing:
  - `¿Cómo incluir asegurados en el cotizador PAC?` retrieved the
    `inclusion de asegurados cotizador` family first.
  - `¿Cómo gestionar formularios web de novedades PAC?` retrieved the
    `formularios web novedades` family first.
- No narrow routing rule was added in this slice because the first live
  retrieval pass already stayed within the intended document families.
