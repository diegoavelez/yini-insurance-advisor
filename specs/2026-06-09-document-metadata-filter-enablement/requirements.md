# Requirements

## Feature Summary

This feature defines the fifth narrow slice of
`Phase 18 — Corpus Metadata and Retrieval Traceability`.

The goal is to re-enable the smallest truthful subset of retrieval-facing
metadata filters now that operator-curated `document_type` and `product` values
already propagate into indexed payloads.

## In Scope

- Allow retrieval queries to filter on curated `document_type` metadata.
- Allow retrieval queries to filter on curated `product` metadata.
- Preserve the existing supported `document_name` and `version` filter behavior.
- Add focused regression coverage for supported metadata filter mapping.

## Out of Scope

- Automatic taxonomy inference or normalization.
- UI controls for metadata filters.
- Additional metadata fields beyond `document_type` and `product`.
- Broader retrieval-ranking changes.

## Acceptance Criteria

- Retrieval no longer rejects `document_type` filters when those values are
  present in indexed payloads.
- Retrieval no longer rejects `product` filters when those values are present
  in indexed payloads.
- Supported filters map deterministically into the Qdrant query filter.
- Regression coverage distinguishes supported metadata filters from any still
  unsupported future metadata fields.
