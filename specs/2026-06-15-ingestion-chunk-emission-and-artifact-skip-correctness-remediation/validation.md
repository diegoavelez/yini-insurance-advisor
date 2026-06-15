# Validation

This slice is ready when the currently failing ingestion behaviors are restored
without reopening unrelated seams.

## Planned Checks

1. `./.venv/bin/python -m pytest -q tests/test_ingestion.py::test_build_chunk_records_prefixes_missing_section_context_for_follow_on_chunks tests/test_ingestion.py::test_successful_ingestion_writes_deterministic_artifacts tests/test_ingestion.py::test_ingestion_applies_operator_curated_metadata_overlay tests/test_ingestion.py::test_ingestion_infers_product_from_source_relative_path_when_overlay_missing tests/test_ingestion.py::test_ingestion_infers_document_type_from_source_relative_path_when_overlay_missing tests/test_ingestion.py::test_existing_outputs_are_skipped_when_overwrite_is_false`
2. `./.venv/bin/python -m pytest -q tests/test_ingestion.py::test_existing_outputs_are_regenerated_when_metadata_is_stale tests/test_ingestion.py::test_build_chunk_records_does_not_duplicate_existing_section_context`
3. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py specs/2026-06-15-ingestion-chunk-emission-and-artifact-skip-correctness-remediation --ignore E501`

## Expected Evidence

- minimal converted markdown now yields at least one chunk;
- follow-on section chunks split with prefixed section context preserved;
- success-path ingestion artifacts again contain chunk records with propagated
  metadata;
- legacy artifacts skip correctly under `overwrite=false`;
- explicit stale-metadata refresh still regenerates artifacts.
