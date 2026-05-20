# Plan

## Status

- Completed on `2026-05-20`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

## Decision

- Selected target:
  - `query classification`
- Rationale:
  - the repo already has deterministic seams for `query_scope` and
    `prompt_guardrails`;
  - the current 30-question evaluation assets can measure this target directly;
  - this is a narrower and lower-risk first DSPy target than answer drafting or
    retrieval routing.
- Baseline quality surface:
  - exact-match rate against `ExpectedBehavior` over the 30-question evaluation
    set;
  - per-category exact-match rate across grounded QA, unsupported, prompt
    injection, citation guardrail, and confidence guardrail scenarios.
- Baseline latency surface:
  - wall-clock duration of `run_local_evaluation()`;
  - derived per-question average duration from the local evaluation run.
- Baseline cost surface:
  - zero external model calls for the current deterministic classification seam;
  - future DSPy slices must report incremental model-call or token-cost surface
    relative to that baseline.

1. Candidate Review
   - Review the roadmap-recommended optimization targets.
   - Select the narrowest defensible first target.

2. Baseline Definition
   - Define the baseline quality metric surface for the selected target.
   - Define the baseline latency and cost reporting surface.

3. Decision Recording
   - Record the target-selection rationale and baseline contract.
   - Keep the output narrow enough for the next DSPy slice.

4. Validation
   - Verify that the decision is explicit and reviewable.
   - Confirm the slice stops before implementation work.
