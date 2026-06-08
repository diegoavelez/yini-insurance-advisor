# Validation

## Status

- Completed on `2026-06-08`.
- Checks passed:
  - `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
  - `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
  - `./.venv/bin/python -m rag.ingestion ingest-pdfs --input-dir data/raw --markdown-dir data/markdown --processed-dir data/processed --manifest-path data/processed/ingestion-manifest.jsonl --overwrite true --fail-fast false`

## Required Checks

- Run a minimal startup/import diagnostic for the current ingestion runtime.
- Run the chosen PDF-to-markdown ingestion path on sample files.

## Required Scenarios

- The current Docling startup block is reproducible and documented.
- The chosen remediation or fallback path generates markdown artifacts for
  sample PDFs.
- The remediation remains scoped to local ingestion runtime behavior.

## Recorded Evidence

- Minimal import diagnostics showed the runtime stalling through the Docling →
  Transformers → Hugging Face Hub import path before practical local conversion
  could begin.
- Earlier ingestion attempts recorded failed Docling-side outcomes in
  `data/processed/ingestion-manifest.jsonl`, including model-download errors for
  RapidOCR assets.
- The implemented PDFium fallback path successfully generated markdown,
  cleaned-markdown, processed-metadata, and chunk artifacts for the four sample
  PDFs under `data/raw/`.

## Merge Readiness

This spec is ready when the repo regains a practical local PDF-to-markdown path
for sample ingestion, with:

- root-cause evidence;
- a documented remediation decision;
- working artifact generation.
