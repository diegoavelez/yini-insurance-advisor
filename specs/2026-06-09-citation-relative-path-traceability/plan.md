# Plan

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.
- Verification recorded in `validation.md`.

1. Contract Enrichment
   - Add the smallest optional relative-path fields required by citations and
     documentary-basis items.

2. Mapping Propagation
   - Reuse existing retrieved-chunk metadata to populate the new fields without
     changing retrieval ranking or answer flow behavior.

3. Regression Coverage
   - Add focused tests for present and absent relative-path cases across the
     citation-facing seams.
