# Requirements

## Feature Summary

This feature defines an additional narrow implementation slice of
`Phase 15 — Final Evaluation and Cleanup`.

The goal is to remove English-copy coupling from the Spanish demo UI state
derivation logic. The UI should derive degraded/support outcomes from stable
typed result fields and structured signals, not from English backend
substrings.

This slice must stay focused on UI state derivation hardening.

## In Scope

- Audit the current UI state derivation logic for English substring coupling.
- Replace brittle English phrase matching with typed or structured result
  signals where feasible.
- Add or update targeted tests that prove Spanish-facing backend/refusal wording
  does not break UI state classification.
- Preserve the current user-visible Spanish UI surfaces unless a wording change
  is required by the hardening itself.

## Out of Scope

- Broader README or roadmap synchronization.
- Retrieval, embeddings, or evaluation-dataset changes.
- Prompt/completion generation redesign.
- Backend contract redesign beyond the minimum seam needed to stop deriving
  state from English copy.
- Hosted deployment changes.

## Alignment Expectations

At minimum:

- Spanish-facing UI state derivation must not depend on English backend copy to
  classify degraded or refusal paths;
- the hardening should preserve current result contracts as much as possible;
- the slice should remain narrow and avoid reopening broader Spanish migration
  work.

## Acceptance Criteria

- UI state derivation no longer relies on English limited-evidence/refusal
  substrings where typed or structured signals are available.
- Targeted regression tests cover Spanish-facing backend/refusal wording.
- Existing UI state behavior remains stable for current success, refusal, and
  degraded paths.
- The slice stops before broader README/roadmap sync work.
