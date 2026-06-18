# Requirements — mvp-go-live-operational-baseline

## Context

The current MVP build-out is technically complete:

- `Phase 0` through `Phase 19` are marked complete;
- the deterministic release gate is now `make test-release`;
- deployment notes, rollback notes, hosted smoke expectations, and the
  evaluation baseline already exist.

What is still missing for a practical MVP handoff is one explicit operational
closure slice that turns those separate assets into a single go-live posture.

Today the repository still spreads that posture across multiple documents:

- `README.md` contains deployment, rollback, hosted-smoke, and runtime notes;
- `docs/evaluation-report.md` contains the deterministic release baseline;
- `docs/category-onboarding-playbook.md` contains corpus-update operations.

That is enough for engineering continuity, but it is not yet one narrow,
explicit go-live baseline for the MVP.

## Goal

Define the operational baseline required to release and run the current MVP
responsibly without expanding product scope.

## In Scope

- define the minimum go-live checklist for the current MVP;
- define the minimum post-deploy hosted validation for the Hugging Face Space;
- define the minimum corpus-update and rollback posture for the current demo;
- identify the supported category set that the MVP is explicitly shipping with.

## Out of Scope

- onboarding new document categories;
- broad product expansion beyond the current demo boundary;
- new runtime integrations or architecture changes;
- fresh retrieval-correction work unless a true blocking regression is found.

## Acceptance Criteria

1. The repository contains one explicit MVP go-live operational baseline.
2. The baseline ties together:
   - the deterministic release gate;
   - the hosted smoke checks;
   - the rollback posture;
   - the corpus-update/operator posture.
3. The baseline names the currently supported category set for the shipped MVP.
4. The baseline stays operational and documentation-sized rather than becoming
   a new product-expansion roadmap.
