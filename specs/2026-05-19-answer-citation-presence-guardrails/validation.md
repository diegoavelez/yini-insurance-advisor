# Validation

## Status

- Implementation complete on `2026-05-19`.
- Verification completed with:
  - `ruff check .`
  - `pytest`

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- A cited answerable response still passes through normally.
- An answerable response without citations is downgraded into a conservative typed guarded outcome.
- The guarded outcome does not fabricate citations.
- Citation-presence guardrail decisions remain observable and correlated when request ids are present.
- The implementation remains scoped to citation-presence guardrails only.

## Merge Readiness

This spec is ready when the next `Phase 9` slice is decision-complete for:

- mandatory citation presence for answerable responses;
- conservative typed downgrade behavior when citations are missing;
- preserved guardrail observability;

without drifting into confidence-policy, prompt-injection, or broader abuse-case work.
