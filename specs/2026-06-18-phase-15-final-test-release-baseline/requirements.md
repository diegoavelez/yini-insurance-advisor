# Requirements — phase-15-final-test-release-baseline

## Context

`Phase 15 — Final Evaluation and Cleanup` already has a durable evaluation
baseline in `docs/evaluation-report.md`, broad regression coverage under
`tests/`, and operator-facing deployment notes in `README.md`. However, the
deliverable `final tests` is still not expressed as one explicit, authoritative
MVP release gate.

Today the repository has the building blocks for final verification, but it
does not yet define:

- which exact commands constitute the official final MVP verification pass;
- which subset is mandatory before release;
- which surfaces each command protects;
- which broader or slower suites remain intentionally outside that release gate.

That leaves the project with strong coverage but an ambiguous final-check
contract.

## Goal

Define a narrow final-test release baseline for the MVP so the repository has a
single documented verification surface for pre-release checks.

## In Scope

- identify the smallest truthful set of release-gate commands for the current
  MVP;
- map those commands to the surfaces they protect;
- distinguish the final MVP release gate from broader non-gating test coverage;
- synchronize roadmap traceability for this remaining `Phase 15` gap.

## Out of Scope

- broad test-suite redesign;
- new external live validation against Qdrant Cloud or Groq;
- performance benchmarking beyond already committed smoke surfaces;
- corpus expansion or new ingestion categories;
- additional `rag` decoupling or architectural refactors.

## Acceptance Criteria

1. The repository defines one documented MVP final-test baseline rather than
   relying on `make test` alone.
2. The baseline identifies the minimum authoritative commands required before
   release, with each command tied to a concrete protection surface.
3. The baseline distinguishes mandatory release-gate checks from broader
   optional or slower suites.
4. The roadmap records `phase-15-final-test-release-baseline` as the narrow
   remaining verification slice under the final evaluation/cleanup posture.
5. The slice stays documentation-and-operator-surface sized unless a minimal
   helper target is necessary to make the baseline runnable.
