# Validation

This slice is ready when the repository is prepared for a narrow `PAC 60+`
baseline onboarding without broadening into the full `EPS/PLAN COMPLEMENTARIO
PAC` folder.

## Automated checks

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'pac'`
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'pac'`
- `./.venv/bin/python -m pytest tests/test_query_scope.py -q -k 'pac'`

## Canonical operator sequence

- Warm-up:
  - `make batch-warmup BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_SAMPLE_PDF="data/raw/EPS/PLAN COMPLEMENTARIO PAC/clausulado pac 60 mas sura v1.pdf"`
- Baseline cohort ingestion, one PDF at a time inside the same logical cohort:
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/clausulado pac 60 mas sura v1.pdf' BATCH_OVERWRITE=false`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/politicas asegurabilidad pac 60 mas.pdf' BATCH_OVERWRITE=false`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/preguntas frecuentes pac 60 mas.pdf' BATCH_OVERWRITE=false`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/tips asesores pac 60 mas v2.pdf' BATCH_OVERWRITE=false`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_GLOB='EPS/PLAN COMPLEMENTARIO PAC/tarifas pac con iva 2026.pdf' BATCH_OVERWRITE=false`

## Deferred cohorts

- Forms / gestión básica:
  - `formulario de afiliacion pac v2.pdf`
  - `formato firma cliente pac v1.pdf`
  - `politica cambio de asesor pac v4.pdf`
  - `tips medios de pago v3.pdf`
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
- Deferred `.docx`:
  - `propuesta renovacion contratos colectivos 60 mas v1.docx`
  - `propuesta renovacion contratos colectivos tradicionales v1.docx`

## Validation notes

- The two large PDF outliers should be run one by one, never inside the
  baseline cohort.
- The two `.docx` files remain explicitly deferred until the ingestion tooling
  supports non-PDF inputs.

## Validation evidence

- `make batch-warmup BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_SAMPLE_PDF="data/raw/EPS/PLAN COMPLEMENTARIO PAC/clausulado pac 60 mas sura v1.pdf"` passed.
- The five baseline PDFs ingested successfully under `overwrite=false`.
- `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_CHUNK_GLOB='eps__plan-complementario-pac__*.chunks.json' BATCH_OVERWRITE=false` passed.
- `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_GLOB='eps__plan-complementario-pac__*.embeddings.json'` passed against Qdrant Cloud.
- Live retrieval checks:
  - `¿Qué tarifas tiene PAC con IVA 2026?` retrieved only `tarifas pac con iva 2026.pdf` chunks.
  - `¿Cuáles son las preguntas frecuentes de PAC 60 Más?` retrieved only `preguntas frecuentes pac 60 mas.pdf` chunks.
  - Initial `¿Qué cubre el PAC 60 Más?` and `¿Qué cubre el clausulado PAC 60 Más?` runs exposed a follow-on policy-family gap.
  - Root-cause review showed the first `clausulado` artifacts were stale: they had been created before the PAC overlays existed and were skipped later by `overwrite=false`, so `document_type` and `product` remained unset in persisted chunk and embedding artifacts.
  - After the stale-artifact regeneration remediation plus PAC policy-family routing rules, the baseline policy queries now resolve correctly:
    - `¿Qué cubre el PAC 60 Más?` retrieves `clausulado pac 60 mas sura v1.pdf` first, anchored at section `9. COBERTURA`.
    - `¿Qué cubre el clausulado PAC 60 Más?` retrieves `clausulado pac 60 mas sura v1.pdf` first, anchored at section `9. COBERTURA`.
    - `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` retrieves `politicas asegurabilidad pac 60 mas.pdf` chunks first.
  - The corrective evidence is now closed in `eps-pac-60-mas-policy-family-coverage-alignment`.
