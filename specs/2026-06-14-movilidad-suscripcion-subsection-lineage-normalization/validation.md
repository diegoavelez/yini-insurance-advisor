# Validation

This slice is ready when collective-policy subsection labels preserve the
correct parent lineage in suscripción artifacts and live retrieval outputs.

## Acceptance Checks

- The new spec bundle exists.
- Focused ingestion coverage proves inconsistent `2.1` / `2.2` child headings
  are normalized under `14. PÓLIZAS COLECTIVAS`.
- Retrieval-facing chunk metadata reflects the normalized subsection lineage.
- At least one live suscripción retrieval result shows the corrected section
  labels.

## Baseline Gap Evidence

- After breadth diversification, live suscripción retrieval now shows broader
  distinct sections first.
- The current cleaned markdown still contains inconsistent collective-policy
  child headings such as:
  - `### 2.1. Facturación agrupada`
  - `### 2.2. Facturación (cobro) agrupada con devolución por asegurado`
  nested under `## 14. PÓLIZAS COLECTIVAS`.
- The remaining gap is therefore subsection-lineage normalization, not ranking
  or family scoping.

## Completion Evidence

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'collective_nested or suscripcion_headings_after_normalization or rewrites_suscripcion'`
  passed after the lineage normalization changes.
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'suscripcion'`
  passed, confirming the earlier suscripción retrieval slices still hold.
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
  passed.
- Rebuilding the suscripción cohort with
  `make batch-ingest BATCH_VENV=./.venv BATCH_PDF_BACKEND=pdfium BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/TRANSVERSALES/*suscripcion*.pdf' BATCH_OVERWRITE=true`
  produced normalized cleaned markdown with:
  - `#### 14.6.1. Facturación agrupada`
  - `#### 14.6.2. Facturación (cobro) agrupada con devolución por asegurado`
- Regenerating embeddings and reindexing the same cohort completed
  successfully.
- Live retrieval for
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'cómo funciona la facturación de pólizas colectivas en movilidad' --product movilidad --document-type policy --top-k 5`
  now returns a result with normalized collective billing lineage:
  - `14.6.2. Facturación (cobro) agrupada con devolución por asegurado`
- A narrower follow-up gap remains: collective billing prompts can still rank
  `13.11. Financiación de Pólizas Individuales` ahead of the more precise
  collective billing subsection, which is now an intent-alignment issue rather
  than a section-lineage issue.
