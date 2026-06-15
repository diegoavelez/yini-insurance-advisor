# Validation

This slice is ready when the three PAC `Global Web` guides are onboarded and
validated without broadening into the remaining PAC folder.

## Automated checks

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'pac and global_web'`
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'pac and (factura or declinacion or asegurados)'`

## Canonical operator sequence

- Warm-up:
  - `make batch-warmup BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_SAMPLE_PDF="data/raw/EPS/PLAN COMPLEMENTARIO PAC/instructivo actualizacion correo para factura global web v2.pdf"`
- Cohort ingestion, one PDF at a time:
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/instructivo actualizacion correo para factura global web v2.pdf' BATCH_OVERWRITE=false`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/instructivo descarga carta de declinacion y pospuestos global web v2.pdf' BATCH_OVERWRITE=false`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/instructivo informe de relacion de asegurados global web v2.pdf' BATCH_OVERWRITE=false`
- Cohort embeddings, one chunk family at a time:
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDINGS_DIR=data/processed/embeddings BATCH_GLOB='eps__plan-complementario-pac__instructivo-actualizacion-correo-para-factura-global-web-v2.chunks.json' BATCH_OVERWRITE=false`
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDINGS_DIR=data/processed/embeddings BATCH_GLOB='eps__plan-complementario-pac__instructivo-descarga-carta-de-declinacion-y-pospuestos-global-web-v2.chunks.json' BATCH_OVERWRITE=false`
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDINGS_DIR=data/processed/embeddings BATCH_GLOB='eps__plan-complementario-pac__instructivo-informe-de-relacion-de-asegurados-global-web-v2.chunks.json' BATCH_OVERWRITE=false`
- Cohort indexing, one embedding family at a time:
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_EMBEDDINGS_DIR=data/processed/embeddings BATCH_MANIFEST_PATH=data/processed/qdrant-indexing-manifest.jsonl BATCH_GLOB='eps__plan-complementario-pac__instructivo-actualizacion-correo-para-factura-global-web-v2.embeddings.json' BATCH_FAIL_FAST=true`
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_EMBEDDINGS_DIR=data/processed/embeddings BATCH_MANIFEST_PATH=data/processed/qdrant-indexing-manifest.jsonl BATCH_GLOB='eps__plan-complementario-pac__instructivo-descarga-carta-de-declinacion-y-pospuestos-global-web-v2.embeddings.json' BATCH_FAIL_FAST=true`
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_EMBEDDINGS_DIR=data/processed/embeddings BATCH_MANIFEST_PATH=data/processed/qdrant-indexing-manifest.jsonl BATCH_GLOB='eps__plan-complementario-pac__instructivo-informe-de-relacion-de-asegurados-global-web-v2.embeddings.json' BATCH_FAIL_FAST=true`
- Retrieval verification:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo actualizar el correo para factura global web en PAC?' --product 'pac' --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo descargar la carta de declinación y pospuestos en PAC?' --product 'pac' --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo obtener el informe de relación de asegurados en PAC?' --product 'pac' --top-k 5`

## Deferred PAC groups

- Long instructivos:
  - `instructivo inclusion de asegurados cotizador v2.pdf`
  - `instructivo formularios web novedades pac v6.pdf`
- Large isolated PDFs:
  - `informacion canales transaccionales y apoyo v1.pdf`
  - `clausulado pac tradicional sura v1.pdf`
- Future PAC policy cohort:
  - `politicas asegurabilidad pac v16.pdf`
- Unsupported `.docx`:
  - `propuesta renovacion contratos colectivos 60 mas v1.docx`
  - `propuesta renovacion contratos colectivos tradicionales v1.docx`

## Validation evidence

- `batch-warmup` succeeded with `clausulado pac 60 mas sura v1.pdf` already cached and
  the cohort sample `instructivo actualizacion correo para factura global web v2.pdf`.
- The three cohort PDFs ingested successfully with `BATCH_OVERWRITE=false`:
  - `instructivo actualizacion correo para factura global web v2.pdf`
  - `instructivo descarga carta de declinacion y pospuestos global web v2.pdf`
  - `instructivo informe de relacion de asegurados global web v2.pdf`
- The three chunk families embedded successfully:
  - `eps__plan-complementario-pac__instructivo-actualizacion-correo-para-factura-global-web-v2.chunks.json`
  - `eps__plan-complementario-pac__instructivo-descarga-carta-de-declinacion-y-pospuestos-global-web-v2.chunks.json`
  - `eps__plan-complementario-pac__instructivo-informe-de-relacion-de-asegurados-global-web-v2.chunks.json`
- The three embedding families indexed successfully into Qdrant Cloud:
  - `eps__plan-complementario-pac__instructivo-actualizacion-correo-para-factura-global-web-v2.embeddings.json`
  - `eps__plan-complementario-pac__instructivo-descarga-carta-de-declinacion-y-pospuestos-global-web-v2.embeddings.json`
  - `eps__plan-complementario-pac__instructivo-informe-de-relacion-de-asegurados-global-web-v2.embeddings.json`
- Processed metadata after onboarding confirmed the intended PAC guide posture:
  - `eps__plan-complementario-pac__instructivo-actualizacion-correo-para-factura-global-web-v2` resolved to `document_name="Instructivo para actualizar correo para envío factura Plan Complementario EPS SURA"`, `product="pac"`, `document_type="guide"`
  - `eps__plan-complementario-pac__instructivo-descarga-carta-de-declinacion-y-pospuestos-global-web-v2` resolved to noisy extracted `document_name="Objetivo"` but retained `product="pac"` and `document_type="guide"`
  - `eps__plan-complementario-pac__instructivo-informe-de-relacion-de-asegurados-global-web-v2` resolved to `document_name="Instructivo para descargar relación de asegurados Plan Complementario EPS SURA"`, `product="pac"`, `document_type="guide"`
- Initial live retrieval showed one narrow ranking gap:
  - `¿Cómo actualizar el correo para factura global web en PAC?` already ranked the factura guide first
  - `¿Cómo obtener el informe de relación de asegurados en PAC?` already ranked the relación de asegurados guide first
  - `¿Cómo descargar la carta de declinación y pospuestos en PAC?` initially drifted toward `politica cambio de asesor pac v4.pdf`
- Narrow PAC term-equivalence routing was added to keep these operational queries inside the intended guide family without broadening the cohort:
  - `factura + global web` → factura guide `document_name`
  - `declinacion + pospuestos` → current extracted `document_name="Objetivo"`
  - `relacion de asegurados` → relación de asegurados guide `document_name`
- Final live retrieval after routing returned the intended guide family first for all three validation queries.
