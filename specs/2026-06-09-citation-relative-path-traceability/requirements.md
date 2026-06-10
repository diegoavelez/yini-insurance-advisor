# Requirements

## Feature Summary

This feature defines the first narrow slice of
`Phase 19 — Citation Readability and Operator Traceability`.

The goal is to expose the already available `source_pdf_relative_path` through
citation-facing contracts so operators can map answers back to the corpus tree
without relying only on human-readable document names.

## In Scope

- Extend citation-facing response contracts with optional relative-path
  traceability fields.
- Propagate `source_pdf_relative_path` from retrieved chunks into citations and
  documentary-basis entries.
- Preserve compatibility with older retrieval payloads that may not include the
  relative path.
- Add focused regression coverage for citation and documentary-basis mapping.

## Out of Scope

- UI redesign or new citation rendering layouts.
- Path prettification or display-label heuristics.
- New retrieval metadata fields beyond `source_pdf_relative_path`.
- Changes to retrieval ranking, answer wording, or guardrail logic.

## Acceptance Criteria

- Citations can optionally carry `source_pdf_relative_path` when retrieval
  provides it.
- Documentary-basis items can optionally carry `source_pdf_relative_path` when
  retrieval provides it.
- Older payloads without relative-path metadata still work.
- Response-contract and retrieval regression coverage verify the new traceability seam.
