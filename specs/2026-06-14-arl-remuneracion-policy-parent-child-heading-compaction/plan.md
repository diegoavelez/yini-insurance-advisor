# Plan

## Objective

Prevent heading-only overlap chunks from surfacing in ARL remuneration-policy
retrieval without removing substantive chunks.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/2026-06-14-arl-remuneracion-policy-parent-child-heading-compaction/requirements.md`
- `specs/2026-06-14-arl-remuneracion-policy-parent-child-heading-compaction/plan.md`
- `specs/2026-06-14-arl-remuneracion-policy-parent-child-heading-compaction/validation.md`
- `specs/roadmap.md`

## Assumptions

- The remaining noisy ARL remuneration-policy surface is caused by overlap-based
  chunk emission, not by missing cleaning of the markdown corpus.
- A chunk containing only headings is not useful evidence for retrieval or
  grounded answering.

## Risks

- An over-broad filter could drop legitimate short chunks if heading-only
  detection is incorrect.
- Chunk index renumbering after rebuild can change downstream artifact order for
  this one document.

## Verification Strategy

- Add focused ingestion coverage proving heading-only overlap chunks are skipped
  while substantive chunks remain.
- Run targeted `pytest` and `ruff`.
- Rebuild and reindex only the ARL remuneration-policy artifact.
- Run live `retrieve-chunks` to confirm the empty heading-only chunk no longer
  appears for representative remuneration-policy queries.
