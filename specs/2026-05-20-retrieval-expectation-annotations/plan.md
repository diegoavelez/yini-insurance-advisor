# Plan

## Status

- Completed on `2026-05-20`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Contract Definition
   - Define the narrow structure for retrieval expectations.
   - Keep linkage to question ids explicit and deterministic.

2. Annotation Authoring
   - Add retrieval expectations for the curated question set.
   - Preserve clear separation between grounded and refusal/guardrail cases.

3. Validation
   - Validate the retrieval expectation dataset locally.
   - Keep checks deterministic and scoped to retrieval expectations only.
