# Plan

## Objective

Reduce `rag/ingestion.py` coupling by moving the local hybrid-recall and
retrieval-query normalization cluster behind a dedicated `rag` seam while
preserving retrieval behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/local_hybrid_recall.py`
- `tests/test_retrieval.py`
- `tests/test_observability.py`
- `specs/roadmap.md`
- `specs/2026-06-14-rag-local-hybrid-recall-and-query-normalization-seam-extraction/requirements.md`
- `specs/2026-06-14-rag-local-hybrid-recall-and-query-normalization-seam-extraction/plan.md`
- `specs/2026-06-14-rag-local-hybrid-recall-and-query-normalization-seam-extraction/validation.md`

## Assumptions

- The current local lexical recall heuristics are already behaviorally correct
  enough to preserve as-is.
- Existing retrieval tests cover the important lexical normalization, fallback
  scoring, and applicability-dedup paths well enough to catch drift.
- Keeping top-level retrieval orchestration in `rag/ingestion.py` preserves the
  intended seam boundary for now.

## Risks

- The cluster crosses query normalization and local lexical fallback, so partial
  extraction could leave duplicated helpers or constants behind.
- Small scoring changes can alter retrieval order for specialized prompts.
- Pulling orchestration into the new seam would make the slice too broad.

## Verification Strategy

- Run focused retrieval and observability tests.
- Run focused lint on touched files.
- Re-run a live retrieval CLI query against the current collection.
