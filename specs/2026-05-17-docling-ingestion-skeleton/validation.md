# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- The CLI ingestion entrypoint contract specifies one canonical command, its
  required flags, optional flags, and non-zero exit conditions.
- The storage layout contract covers `data/raw/`, `data/markdown/`, and
  `data/processed/`.
- The processed-document contract surface preserves source-to-output traceability.
- The ingestion status vocabulary is explicit and limited.
- Failure reporting fields are explicit for unsuccessful ingestion runs.
- Re-run behavior for `--overwrite=false` and `--overwrite=true` is explicit.
- Docling dependency assumptions include a non-network smoke path or a clear
  failure mode when Docling is unavailable.

## Merge Readiness

This spec is ready when the first Phase 2 slice is decision-complete for a
CLI-first ingestion skeleton without pulling in later cleaning or chunking work.
