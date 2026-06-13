# Plan — Category Onboarding Playbook

## Objective

Capture a durable, operator-facing procedure for onboarding new RAG categories
based on the implemented experience from `AUTOS` and `BICICLETAS Y
PATINETAS`.

## Affected Files

- `docs/category-onboarding-playbook.md`
- `README.md`
- `specs/2026-06-13-category-onboarding-playbook/requirements.md`
- `specs/2026-06-13-category-onboarding-playbook/validation.md`

## Assumptions

- The current batch commands and repository layout are already the
  authoritative execution surface.
- The most valuable addition is durable operator guidance, not new code.
- The roadmap does not need a new phase for this slice because this is
  documentation and operational traceability over already-implemented
  capabilities.

## Risks

- The document could become too abstract if it does not anchor to concrete
  commands and failure modes.
- The document could become misleading if it recommends broad fixes instead of
  narrow corrective slices.

## Implementation Steps

1. Document the end-to-end category onboarding flow in `docs/`.
2. Encode the taxonomy, artifact, and validation gates explicitly.
3. Capture lessons learned from `AUTOS` and `BICICLETAS Y PATINETAS`.
4. Link the playbook from the `README.md` ingestion/runtime surface.
5. Record validation as a documentation review against current commands and
   repository paths.

## Verification Strategy

- verify that referenced commands and paths match current repository surfaces;
- verify that the README link points to the new playbook;
- verify that the playbook distinguishes ingestion, retrieval, and
  grounded-answer readiness.
