# Requirements

## Feature Summary

This feature defines the fourth narrow slice of
`Phase 19 — Citation Readability and Operator Traceability`.

The goal is to expose already curated `document_type` and `product` metadata in
citation-facing operator surfaces so reviewers can distinguish document class
and product context without leaving the current grounded-response UI.

## In Scope

- Extend citation-facing response contracts with optional `document_type` and
  `product` fields where the retrieval seam already knows them.
- Propagate curated `document_type` and `product` from retrieved chunks into
  citations and documentary-basis items.
- Render those fields in the current Gradio `Citas` and `Base documental`
  surfaces with stable Spanish labels.
- Add focused contract, grounded-answer, and UI regression coverage for present
  and absent metadata cases.

## Out of Scope

- New retrieval filters or UI filter controls.
- Automatic taxonomy inference or metadata normalization.
- Broad layout redesign or clickable document navigation.
- Changes to ranking, prompting, or answer wording.

## Acceptance Criteria

- Citations can optionally carry `document_type` and `product` when retrieval
  provides them.
- Documentary-basis items can optionally carry `document_type` and `product`
  when retrieval provides them.
- The Gradio citation-facing surfaces render those fields when available and
  remain clean when they are absent.
- Focused tests cover contract propagation and UI rendering for both metadata
  presence and absence cases.
