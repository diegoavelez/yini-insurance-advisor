# Plan

## Objective

Extend Qdrant bootstrap payload-index creation to include `document_name` so
live retrieval can use the new PV document-family filter.

## Affected Files

- `rag/ingestion.py`
- `tests/test_qdrant_indexing.py`
- `specs/roadmap.md`
- `specs/2026-06-13-qdrant-document-name-filter-index-alignment/requirements.md`
- `specs/2026-06-13-qdrant-document-name-filter-index-alignment/validation.md`

## Assumptions

- the remote collection can receive the new payload index during a normal
  indexing rerun;
- `document_name` uses the same keyword-compatible exact-match semantics as the
  existing indexed metadata fields;
- no retrieval-code changes are needed beyond bootstrap alignment.

## Risks

- assuming the remote collection auto-backfills without an operator rerun;
- broadening the field set beyond the immediate need;
- forgetting to preserve compatibility with clients lacking payload-index
  helpers.

## Steps

1. Extend the bootstrap field set with `document_name`.
2. Update focused indexing tests to reflect the new field set.
3. Update the roadmap and validation notes with the operator rerun requirement.
4. Run targeted tests and lint.

## Verification Strategy

- run focused indexing and retrieval tests;
- run Ruff on touched files;
- hand off the live reindex command for operator execution.
