# Validation

This slice is ready when the four-document PAC operational cohort is onboarded
and validated without broadening into the remaining PAC folder.

## Automated checks

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'pac and (overlay or afiliacion)'`
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'pac'`

## Canonical operator sequence

- Warm-up:
  - `make batch-warmup BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_SAMPLE_PDF="data/raw/EPS/PLAN COMPLEMENTARIO PAC/formulario de afiliacion pac v2.pdf"`
- Cohort ingestion, one PDF at a time:
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/formulario de afiliacion pac v2.pdf' BATCH_OVERWRITE=false`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/formato firma cliente pac v1.pdf' BATCH_OVERWRITE=false`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/politica cambio de asesor pac v4.pdf' BATCH_OVERWRITE=false`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/tips medios de pago v3.pdf' BATCH_OVERWRITE=false`
- Embeddings:
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_CHUNK_GLOB='eps__plan-complementario-pac__formulario-de-afiliacion-pac-v2.chunks.json' BATCH_OVERWRITE=false`
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_CHUNK_GLOB='eps__plan-complementario-pac__formato-firma-cliente-pac-v1.chunks.json' BATCH_OVERWRITE=false`
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_CHUNK_GLOB='eps__plan-complementario-pac__politica-cambio-de-asesor-pac-v4.chunks.json' BATCH_OVERWRITE=false`
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_CHUNK_GLOB='eps__plan-complementario-pac__tips-medios-de-pago-v3.chunks.json' BATCH_OVERWRITE=false`
- Indexing:
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_GLOB='eps__plan-complementario-pac__formulario-de-afiliacion-pac-v2.embeddings.json'`
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_GLOB='eps__plan-complementario-pac__formato-firma-cliente-pac-v1.embeddings.json'`
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_GLOB='eps__plan-complementario-pac__politica-cambio-de-asesor-pac-v4.embeddings.json'`
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_GLOB='eps__plan-complementario-pac__tips-medios-de-pago-v3.embeddings.json'`

## Deferred PAC groups

- Short Global Web guides:
  - `instructivo actualizacion correo para factura global web v2.pdf`
  - `instructivo descarga carta de declinacion y pospuestos global web v2.pdf`
  - `instructivo informe de relacion de asegurados global web v2.pdf`
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

- `make batch-warmup BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_SAMPLE_PDF="data/raw/EPS/PLAN COMPLEMENTARIO PAC/formulario de afiliacion pac v2.pdf"` passed.
- The four operational PAC PDFs ingested successfully under `overwrite=false`.
- The four chunk bundles generated embeddings successfully under `overwrite=false`.
- The four embedding bundles indexed successfully against Qdrant Cloud.
- Processed document metadata resolved as expected:
  - `formulario de afiliacion pac v2.pdf` → `SOLICITUD DE AFILIACIÓN PARA PLANES COMPLEMENTARIOS` / `form` / `pac`
  - `formato firma cliente pac v1.pdf` → `CONFIRMACIÓN DEL CONTENIDO DE LA SOLICITUD ELECTRÓNICA DE SEGURO` / `form` / `pac`
  - `politica cambio de asesor pac v4.pdf` → `PAC EPS SURA - Política Cambio de Asesor` / `policy` / `pac`
  - `tips medios de pago v3.pdf` → `Por eso queremos presentarte los medios de pago que más se ajustan a sus necesidades.` / `guide` / `pac`
- Initial live retrieval showed that the affiliation and client-signature queries drifted into the change-of-advisor policy family.
- A narrow PAC operational routing rule was then added through the existing term-equivalence seam for:
  - affiliation form intent
  - client-signature form intent
  - change-of-advisor policy intent
  - payment-media guide intent
- Final live retrieval checks:
  - `¿Cómo diligencio el formulario de afiliación PAC?` now retrieves the `formulario de afiliacion pac v2.pdf` family first.
  - `¿Cómo funciona el formato de firma del cliente PAC?` now retrieves the `formato firma cliente pac v1.pdf` family first.
  - `¿Cómo se hace el cambio de asesor en PAC?` retrieves the `politica cambio de asesor pac v4.pdf` family first.
  - `¿Qué medios de pago tiene PAC?` retrieves the `tips medios de pago v3.pdf` family first.
