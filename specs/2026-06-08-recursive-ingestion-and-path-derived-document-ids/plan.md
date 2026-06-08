# Plan

## Status

- Planned on `2026-06-08`.
- Completed on `2026-06-08`.
- Verification recorded in `validation.md`.

1. Recursive Discovery
   - Extended source PDF discovery to support nested folders under the input
     directory.
   - Kept CLI behavior explicit and deterministic.

2. Stable Path-Derived Identity
   - Introduced a collision-safe document id derived from the source path
     relative to the input directory.
   - Used that id consistently for markdown, processed metadata, and chunk
     artifacts.

3. Validation
   - Added tests for nested-folder discovery and duplicate-basename handling.
   - Validated sample local ingestion against a nested real-world folder
     fixture.
