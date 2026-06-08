# Plan

## Status

- Planned on `2026-06-08`.
- Completed on `2026-06-08`.
- Verification recorded in `validation.md`.

1. Policy Wiring
   - Added explicit backend-selection controls for local ingestion.
   - Set the default local policy to Docling-first.

2. Warm-Up and Timeout
   - Added a Docling warm-up path for asset download.
   - Made the Docling startup timeout practical and configurable.

3. Validation
   - Added targeted tests for backend mode and warm-up behavior.
   - Verified local sample ingestion still works under the chosen policy.
