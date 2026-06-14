# Plan

## Objective

Leave a durable roadmap trail for the next non-urgent `rag` decoupling slices
so they can be evaluated after the current category-onboarding wave.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-14-rag-post-onboarding-coupling-slices/requirements.md`
- `specs/2026-06-14-rag-post-onboarding-coupling-slices/plan.md`
- `specs/2026-06-14-rag-post-onboarding-coupling-slices/validation.md`

## Assumptions

- the current lexical seam extraction is sufficient for near-term coupling
  containment;
- the remaining refactors are best treated as deferred architecture work until
  more categories are onboarded.

## Risks

- accidentally making deferred slices look like current MVP blockers;
- documenting candidates too vaguely to be useful later.

## Steps

1. Name the deferred `rag` coupling slices explicitly.
2. Add a roadmap note that they are post-onboarding refactor candidates.
3. Keep the currently active retrieval/onboarding status unchanged.

## Verification Strategy

- inspect the updated roadmap section for the new deferred-candidate note;
- confirm the current implementation-status list remains unchanged apart from
  the added deferred note.
