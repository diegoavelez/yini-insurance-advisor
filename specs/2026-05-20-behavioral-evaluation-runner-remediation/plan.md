# Plan

## Status

- Completed on `2026-05-20`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Ownership Cleanup
   - Resolve whether golden expected behavior lives in the question set or the
     dedicated golden dataset.
   - Remove the duplicate source of truth.

2. Runner Remediation
   - Replace tautological `actual_behavior` derivation with a defensible
     evaluation seam.
   - Preserve deterministic typed results.

3. Contract Tightening
   - Expose explicit expectation-dataset versions in run results.
   - Keep the result shape reviewable and locally testable.

4. Validation
   - Add tests for the corrected ownership model and non-tautological runner
     behavior.
   - Keep checks scoped to the evaluation seam correction.
