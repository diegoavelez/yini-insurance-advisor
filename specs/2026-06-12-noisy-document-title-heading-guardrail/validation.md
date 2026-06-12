# Validation

## Status

- Planned on `2026-06-12`.
- Code completed on `2026-06-12`.

## Required Checks

- Noisy media/embed headings are rejected for `document_name` promotion.
- Deterministic fallback to the filename stem still works.
- Existing safe heading extraction remains intact.

## Required Scenarios

- A normal heading still becomes `document_name`.
- A heading such as `Grabación: https://...` is rejected and falls back to the
  PDF stem.

## Merge Readiness

This slice is ready when retrieval-facing document labels no longer promote
obviously noisy media/embed headings and the fallback remains deterministic.

## Evidence

- Focused ingestion validation passed:
  - `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
  - `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- Regression coverage now includes a noisy ARL-style heading:
  - `Grabación: https://...`
  - expected fallback: PDF stem

## Operator Follow-up

- Existing processed artifacts keep the old `document_name` until the affected
  documents are regenerated and reindexed.
- For the current ARL corpus, rerun:
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json BATCH_OVERWRITE=true`
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed BATCH_OVERWRITE=true`
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed`
