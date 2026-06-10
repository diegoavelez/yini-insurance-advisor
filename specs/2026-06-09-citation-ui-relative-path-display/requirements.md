# Requirements

## Feature Summary

This feature defines the second narrow slice of
`Phase 19 — Citation Readability and Operator Traceability`.

The goal is to expose the already propagated `source_pdf_relative_path` in the
current public demo citation rendering so operators can see the corpus-relative
source location directly in the UI.

## In Scope

- Extend the current citation markdown renderer to include
  `source_pdf_relative_path` when it is available.
- Use one stable Spanish-facing label for the rendered relative path.
- Preserve clean fallback behavior when the relative path is absent.
- Add focused UI rendering regression coverage for citations with and without
  relative-path metadata.

## Out of Scope

- Broad layout redesign of the demo UI.
- Path prettification, shortening, or relabeling heuristics.
- Changes to response contracts or retrieval behavior.
- New operator navigation controls or clickable file browsing.

## Acceptance Criteria

- Rendered citations include `source_pdf_relative_path` when present.
- Rendered citations remain stable and readable when the field is absent.
- The change remains localized to the existing citation formatting seam.
- Focused UI tests cover both presence and absence of the relative path.
