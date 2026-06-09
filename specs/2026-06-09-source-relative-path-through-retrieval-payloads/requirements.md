# Requirements

## Feature Summary

This feature defines the second narrow slice of
`Phase 18 — Corpus Metadata and Retrieval Traceability`.

The goal is to preserve raw-source traceability through the vector payload and
retrieval-result seams so later operator tooling, retrieval inspection, and
metadata-enrichment work do not lose the original relative source location.

## In Scope

- Add `source_pdf_relative_path` to the embedding payload contract.
- Persist `source_pdf_relative_path` into Qdrant payloads during indexing.
- Map `source_pdf_relative_path` back into retrieved chunk results when present.
- Keep the slice narrow to retrieval-facing traceability only.

## Out of Scope

- New retrieval filters.
- Citation format changes.
- UI changes.
- Metadata normalization beyond propagating the existing relative path field.

## Acceptance Criteria

- `source_pdf_relative_path` is carried from chunk records into embedding
  payloads and Qdrant payloads.
- Retrieved chunks expose `source_pdf_relative_path` when the payload includes
  it.
- Existing retrieval behavior still works when older payloads do not include
  the new field.
