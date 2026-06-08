# Plan

## Status

- Completed on `2026-06-08`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Fixture Audit
   - Review evaluation questions, expectations, and optimization-subset linkage.
   - Identify tests pinned to current dataset versions.

2. Spanish Fixture Alignment
   - Translate the curated evaluation prompts.
   - Translate the linked optimization subset prompts to keep exact alignment.

3. Smoke Coverage
   - Update hosted-like smoke checks to exercise Spanish-facing requests.
   - Confirm local evaluation remains matched.

4. Validation
   - Update deterministic tests for versions and fixture content.
   - Run evaluation and smoke coverage tests.
