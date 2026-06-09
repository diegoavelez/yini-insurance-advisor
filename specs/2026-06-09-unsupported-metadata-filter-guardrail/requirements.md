# Requirements

## Feature Summary

This feature defines the third narrow slice of
`Phase 18 — Corpus Metadata and Retrieval Traceability`.

The goal is to stop the retrieval and answer paths from accepting metadata
filters that the current indexed corpus cannot actually satisfy, avoiding
silent false-negative retrieval results.

## In Scope

- Make the current supported metadata-filter surface explicit.
- Guard the retrieval and grounded-answer paths against unsupported
  `document_type` and `product` filters while preserving supported filters that
  are backed by current payload fields.
- Add focused validation for the guarded unsupported-filter behavior.

## Out of Scope

- Adding new metadata extraction for `document_type` or `product`.
- UI redesign.
- Reworking `document_name` or `document_version` filtering behavior.
- Broader corpus-enrichment logic.

## Acceptance Criteria

- Retrieval no longer silently applies unsupported `document_type` or
  `product` filters against payloads that do not carry those fields.
- Supported filters remain available where the current payload contract
  actually supports them.
- The failure mode for unsupported metadata filters is explicit and testable.
