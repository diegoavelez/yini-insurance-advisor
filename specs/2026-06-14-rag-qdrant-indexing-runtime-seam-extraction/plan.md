# Plan

## Objective

Reduce `rag/ingestion.py` coupling further by moving the remaining
Qdrant-specific indexing runtime helpers into `rag/qdrant_store.py` while
preserving indexing behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/qdrant_store.py`
- `tests/test_qdrant_indexing.py`
- `specs/roadmap.md`
- `specs/2026-06-14-rag-qdrant-indexing-runtime-seam-extraction/requirements.md`
- `specs/2026-06-14-rag-qdrant-indexing-runtime-seam-extraction/plan.md`
- `specs/2026-06-14-rag-qdrant-indexing-runtime-seam-extraction/validation.md`

## Assumptions

- The remaining retry/prune/smoke helpers are already behaviorally correct and
  should move without semantic changes.
- Existing indexing tests cover the failure and retry paths well enough to
  detect contract drift.
- Keeping manifest-record construction in `rag/ingestion.py` preserves the
  current orchestration boundary.

## Risks

- Partial extraction could leave one helper split across modules and weaken the
  seam.
- Changing retry or prune behavior would alter live indexing semantics against
  the existing cloud collection.
- Over-expanding into embedding-generation orchestration would blur the slice.

## Verification Strategy

- Run focused Qdrant indexing tests.
- Run focused lint on touched files.
- Re-run one live retrieval or answer command to confirm the extended seam
  still interoperates with the real Qdrant runtime.
