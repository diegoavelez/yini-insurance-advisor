# Validation

## Status

- Planned on `2026-06-12`.
- Completed on `2026-06-12`.

## Required Checks

- The repository exposes a minimal operator-facing surface for the external
  batch runtime.
- The documented commands remain aligned to the existing ingestion CLI.
- At least one real batch target executes against the validated external
  runtime with temporary output paths.

## Required Scenarios

- An operator can point batch commands at a configurable external venv.
- An operator can run Docling warm-up without touching the app runtime flow.
- An operator can run ingestion and embeddings against temporary outputs.

## Merge Readiness

This slice is ready when the external local batch workflow is documented,
discoverable, configurable, and validated against the already proven runtime
path.

## Evidence

- Target expansion stays aligned to the canonical ingestion CLI:
  - `make -n batch-warmup batch-ingest batch-embeddings batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_MARKDOWN_DIR=/tmp/yini-batch-makecheck/markdown BATCH_PROCESSED_DIR=/tmp/yini-batch-makecheck/processed`
- The new operator-facing `Makefile` targets were validated against the already
  proven external runtime path:
  - `make batch-warmup BATCH_VENV=/private/tmp/yini-fast-venv311`
  - `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_MARKDOWN_DIR=/tmp/yini-batch-makecheck/markdown BATCH_PROCESSED_DIR=/tmp/yini-batch-makecheck/processed`
  - `make batch-embeddings BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=/tmp/yini-batch-makecheck/processed`
- The real validated batch run used temporary outputs rather than committed repo
  artifacts:
  - markdown output under `/tmp/yini-batch-makecheck/markdown`
  - processed output under `/tmp/yini-batch-makecheck/processed`
- The validated ingestion target completed successfully against the current
  four-PDF sample tree using `Docling`.
- The validated embeddings target completed successfully against the temporary
  chunk outputs using the external runtime.

## Recorded Outcome

- The repository now exposes a narrow, repeatable, configurable external batch
  operator flow without changing the app runtime contract.
- Heavy local batch work can stay on the validated external venv while the repo
  keeps `.venv` for app/test workflows.
- Temporary local artifacts remain outside the commit surface by default.
