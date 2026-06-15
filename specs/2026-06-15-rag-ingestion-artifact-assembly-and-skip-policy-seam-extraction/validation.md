# Validation

This slice is ready when artifact assembly and per-document skip policy live
behind their own `rag` seam and validated ingestion behavior remains unchanged.

## Status

- Completed on `2026-06-14`.
- Checks passed:
  - `./.venv/bin/python -m ruff check rag/ingestion.py rag/ingestion_artifacts.py tests/test_ingestion.py specs/2026-06-15-rag-ingestion-artifact-assembly-and-skip-policy-seam-extraction --ignore E501`
  - `./.venv/bin/python -m pytest -q tests/test_ingestion.py`

## Planned Checks

1. `./.venv/bin/python -m pytest -q tests/test_ingestion.py::test_successful_ingestion_writes_deterministic_artifacts tests/test_ingestion.py::test_ingestion_applies_operator_curated_metadata_overlay tests/test_ingestion.py::test_ingestion_infers_product_from_source_relative_path_when_overlay_missing tests/test_ingestion.py::test_ingestion_infers_document_type_from_source_relative_path_when_overlay_missing tests/test_ingestion.py::test_existing_outputs_are_skipped_when_overwrite_is_false tests/test_ingestion.py::test_existing_outputs_are_regenerated_when_metadata_is_stale`
2. `./.venv/bin/python -m pytest -q tests/test_ingestion.py::test_build_chunk_records_prefixes_missing_section_context_for_follow_on_chunks tests/test_ingestion.py::test_build_chunk_records_does_not_duplicate_existing_section_context tests/test_ingestion.py::test_build_chunk_records_with_large_section_body_uses_overlap_windows`
3. `./.venv/bin/python -m ruff check rag/ingestion.py rag/ingestion_artifacts.py tests/test_ingestion.py specs/2026-06-15-rag-ingestion-artifact-assembly-and-skip-policy-seam-extraction --ignore E501`

## Expected Evidence

- chunk bundles still emit chunks with the expected section context and
  metadata;
- embedding-compatible bundle construction still preserves payload metadata;
- `overwrite=false` still skips compatible/legacy artifacts and refreshes stale
  metadata when explicitly requested;
- wrappers in `rag.ingestion.py` still preserve the current test patch points.
