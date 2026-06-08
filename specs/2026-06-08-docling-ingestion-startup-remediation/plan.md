# Plan

## Status

- Completed on `2026-06-08`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Root-Cause Evidence
   - Reproduce the Docling startup block in a minimal import path.
   - Capture where the runtime stalls.

2. Narrow Remediation
   - Choose the smallest safe remediation or approved fallback path.
   - Keep the existing ingestion contract stable unless a minimal seam change is required.

3. Validation
   - Verify that sample PDFs can produce markdown artifacts through the chosen path.
   - Confirm the remediation is documented and repeatable.
