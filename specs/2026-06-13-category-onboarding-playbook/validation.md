# Validation — Category Onboarding Playbook

## Expected Result

The repository contains one durable category-onboarding playbook that matches
the current ingestion and batch-runtime surfaces.

## Checks

- `docs/category-onboarding-playbook.md` exists and documents:
  - raw folder taxonomy;
  - ingestion to indexing workflow;
  - inspection gates;
  - symptom-to-action mapping;
  - criteria for opening narrow corrective specs.
- `README.md` points to `docs/category-onboarding-playbook.md` from the
  ingestion/batch-runtime section.
- All referenced commands and paths match current repository surfaces:
  - `make batch-warmup`
  - `make batch-ingest`
  - `python -m rag.ingestion ingest-pdfs`
  - `python -m rag.ingestion generate-embeddings`
  - `python -m rag.ingestion index-embeddings`

## Notes

- No runtime code changed in this slice.
- No automated tests are required beyond documentation consistency review.
