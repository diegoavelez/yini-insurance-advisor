# Plan

## Objective

Reduce `rag/ingestion.py` coupling by extracting the stabilized Qdrant payload,
filter, and bootstrap cluster into a dedicated module while preserving
indexing/retrieval behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/qdrant_store.py`
- `specs/roadmap.md`
- `specs/2026-06-14-rag-qdrant-client-and-payload-seam-extraction/requirements.md`
- `specs/2026-06-14-rag-qdrant-client-and-payload-seam-extraction/plan.md`
- `specs/2026-06-14-rag-qdrant-client-and-payload-seam-extraction/validation.md`

## Assumptions

- The current Qdrant payload contract is correct and should be preserved.
- Client compatibility behavior for environments exposing either `search()` or
  `query_points()` remains part of the Qdrant seam rather than a ranking seam.
- Existing retrieval and indexing tests already cover enough behavior to detect
  accidental contract drift.

## Risks

- Moving only part of the Qdrant cluster could leave hidden model-construction
  dependencies in `rag/ingestion.py`.
- Changing payload keys or filter mappings, even unintentionally, would break
  live retrieval and prune/index flows against the current collection.
- Over-expanding the slice into retrieval ranking would make validation much
  harder and blur the seam boundary.

## Verification Strategy

- Run focused retrieval/indexing tests that touch Qdrant payload/filter
  behavior.
- Run focused lint on touched files.
- Re-run one live retrieval query and one live grounded-answer query against the
  current cloud collection to confirm the seam still interoperates with the
  real Qdrant runtime.
