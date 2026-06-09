# Requirements

## Feature Summary

This feature defines the fourth narrow slice of
`Phase 18 — Corpus Metadata and Retrieval Traceability`.

The goal is to introduce a narrow operator-curated metadata seam so the corpus
can carry truthful `document_type` and `product` metadata without relying on
unsafe filename heuristics or silent unsupported filters.

## In Scope

- Define a small operator-maintained metadata overlay input keyed by the current
  stable document identity surface.
- Apply overlay values to the current ingestion/processed-document metadata path.
- Propagate curated `document_type` and `product` values only where the current
  payload and retrieval seams can preserve them deterministically.
- Keep overlay behavior optional so documents without curated metadata still
  ingest successfully.

## Out of Scope

- Automatic classification of documents into product/type groups.
- UI editing for metadata.
- Broad corpus taxonomy design beyond the minimum fields needed now.
- Changes to answer wording or citation formatting.

## Acceptance Criteria

- The repository has one explicit operator-curated seam for `document_type` and
  `product`.
- Overlay data is keyed by stable corpus identity rather than ad hoc filename
  matching.
- Documents without overlay entries continue to work.
- The slice creates a truthful foundation for eventually re-enabling richer
  metadata filters.
