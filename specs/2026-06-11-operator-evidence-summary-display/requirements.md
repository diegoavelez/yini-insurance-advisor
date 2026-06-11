# Requirements

## Feature Summary

This feature defines the fifth narrow slice of
`Phase 19 — Citation Readability and Operator Traceability`.

The goal is to surface a compact operator-facing evidence summary that makes it
quick to understand which documents, document types, and products supported the
current grounded draft without manually parsing the full citation blocks.

## In Scope

- Derive a compact evidence summary from the current grounded-response evidence.
- Surface stable summary fields such as unique document names and, when
  available, curated `document_type` and `product` values.
- Expose the summary in one narrow operator-facing UI surface or existing debug
  seam without broad layout redesign.
- Add focused UI regression coverage for summary-present and summary-empty
  scenarios.

## Out of Scope

- New retrieval contracts or ranking changes.
- New filtering controls or interactive navigation.
- Broad UI redesign or citation prettification.
- Automatic metadata normalization or inference.

## Acceptance Criteria

- The UI exposes a compact evidence summary derived from the current grounded
  evidence.
- The summary includes deduplicated document names and curated metadata where
  available.
- The summary remains clean when evidence is missing or minimal.
- Focused tests cover both evidence-rich and empty-evidence scenarios.
