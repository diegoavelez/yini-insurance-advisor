# Plan

## Status

- Planned on `2026-06-11`.
- Completed on `2026-06-11`.
- Verification recorded in `validation.md`.

1. Contract Review
   - Confirm the smallest citation-facing contract enrichment needed to surface
     already curated retrieval metadata.

2. Propagation and Rendering
   - Reuse existing retrieved-chunk metadata to populate citations and
     documentary basis, then render the new fields in the current UI seams.

3. Regression Coverage
   - Add focused contract, grounded-answer, and UI tests for present and absent
     `document_type` and `product` values.
