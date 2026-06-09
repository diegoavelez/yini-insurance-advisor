# Plan

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.
- Verification will be recorded in `validation.md`.

1. Filter Contract Review
   - Confirm the current retrieval filter surface and isolate the exact fields
     that should move from guarded to supported.

2. Qdrant Mapping Enablement
   - Extend the typed retrieval-to-Qdrant filter mapping for curated
     `document_type` and `product` fields without broadening scope.

3. Regression Coverage
   - Replace rejection-only assertions with focused supported-filter mapping
     checks and preserve current behavior for unrelated retrieval seams.
