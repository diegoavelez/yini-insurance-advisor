# Requirements — Category Onboarding Playbook

## Context

The repository now has practical onboarding evidence from at least two
categories with different failure modes:

- `MOVILIDAD/AUTOS`
- `MOVILIDAD/BICICLETAS Y PATINETAS`

That experience should be captured as durable operator guidance so future
category onboarding does not rely on chat history or implicit project memory.

## Goal

Document the recommended workflow for adding a new corpus category from raw PDF
placement through ingestion, embeddings, Qdrant indexing, retrieval
validation, and grounded-answer validation.

## Scope

This slice should:

1. add one durable playbook under `docs/`;
2. link that playbook from a visible operator-facing surface in `README.md`;
3. encode the main decision points learned from `AUTOS` and `BICICLETAS Y
   PATINETAS`;
4. define when operators should use:
   - raw folder taxonomy;
   - metadata overlays;
   - term-equivalence rules;
   - narrow corrective specs.

## Non-Goals

This slice should not:

- change ingestion code;
- change retrieval code;
- change embeddings or Qdrant behavior;
- redesign the roadmap phases;
- introduce new runtime commands beyond documenting existing ones.

## Acceptance Criteria

1. A new operator can follow the documented route without prior chat context.
2. The document explains the preferred raw folder structure for new
   categories.
3. The document distinguishes ingestion success from retrieval readiness.
4. The document includes a symptom-to-action mapping for common onboarding
   failures.
5. The `README.md` points readers to the new playbook from the ingestion/batch
   workflow surface.
