# Plan

## Objective

Close the runtime gap between supported metadata filters and Qdrant payload
index availability.

## Affected Files

- `rag/ingestion.py`
- `tests/test_qdrant_indexing.py`
- `README.md`
- `Makefile`
- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json`
- `specs/roadmap.md`
- `specs/2026-06-12-qdrant-metadata-filter-index-alignment/requirements.md`
- `specs/2026-06-12-qdrant-metadata-filter-index-alignment/validation.md`

## Assumptions

- current retrieval filters remain intentionally limited to `document_type` and
  `product`;
- creating payload indexes during indexing bootstrap is the narrowest safe
  remediation;
- some Qdrant client surfaces may omit payload-index helpers and should not
  break indexing.

## Risks

- assuming payload-index creation exists on every Qdrant client version;
- leaving roadmap status inconsistent after discovering a real runtime gap;
- mixing unrelated ARL operator-flow changes with the corrective remediation.

## Verification Strategy

- add focused indexing coverage for payload-index creation and compatibility
  fallback;
- run targeted indexing and retrieval tests;
- document the corrective slice in the roadmap.
