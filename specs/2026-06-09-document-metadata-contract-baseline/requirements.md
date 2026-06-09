# Requirements

## Feature Summary

This feature defines the first narrow slice of
`Phase 18 — Corpus Metadata and Retrieval Traceability`.

The goal is to make the current document-metadata gap explicit before changing
retrieval or ingestion behavior, so later corpus-enrichment work can proceed
from a typed and reviewable baseline instead of ad hoc field usage.

## In Scope

- Document the current repository-level metadata responsibilities around:
  - `source_pdf_id`
  - retrieval-facing `document_name`
  - optional `document_version`
  - path-derived traceability from nested raw sources
- Define the minimum baseline contract the next implementation slice must
  preserve or enrich.
- Record the current known limitations without changing behavior yet.

## Out of Scope

- Automatic metadata extraction from filenames or document contents.
- Changes to chunk generation, embedding generation, or Qdrant indexing logic.
- UI changes.
- New retrieval filters.

## Acceptance Criteria

- The baseline metadata contract is explicit and tied to current implemented
  fields.
- The current limitations of `document_name` / `document_version` are recorded
  without overstating implementation.
- The next metadata-enrichment slice can proceed without first rediscovering
  current corpus identity assumptions.
