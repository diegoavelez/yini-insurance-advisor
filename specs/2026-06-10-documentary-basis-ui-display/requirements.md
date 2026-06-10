# Requirements

## Feature Summary

This feature defines the third narrow slice of
`Phase 19 — Citation Readability and Operator Traceability`.

The goal is to expose the already available `documentary_basis` structure in
the current public demo so operators can review source support in a dedicated,
readable UI surface instead of relying on citations alone.

## In Scope

- Add one dedicated UI rendering seam for `documentary_basis` items.
- Render stable documentary-basis fields already present in typed responses,
  including `document_name`, optional `source_pdf_relative_path`, `section`,
  `page`, and `clause_id`.
- Preserve clean fallback behavior when no documentary basis is available.
- Add focused UI regression coverage for documentary-basis rendering.

## Out of Scope

- Broad layout redesign of the demo UI.
- New retrieval metadata or response-contract changes.
- Path prettification or clickable navigation.
- Changes to answer wording, citations, or support-context behavior.

## Acceptance Criteria

- The UI exposes a dedicated documentary-basis output surface.
- Documentary-basis items render stable source-review fields when present.
- The UI remains clean when documentary-basis is empty.
- Focused UI tests cover presence and absence of documentary-basis entries.
