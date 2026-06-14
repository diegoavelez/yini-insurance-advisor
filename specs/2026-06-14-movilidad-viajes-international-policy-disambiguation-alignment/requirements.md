# Requirements

## Title

Align explicit `viaje internacional` policy retrieval with the international
clausulado family.

## Context

The baseline `MOVILIDAD/VIAJES` onboarding is now operational through
ingestion, embeddings, Qdrant indexing, and first retrieval validation.

Live validation exposed a concrete narrow gap:

- the query `qué cubre el clausulado de viaje internacional`
  returned both `CONDICIONADO SEGURO VIAJE NACIONAL` and
  `CONDICIONADO SEGURO VIAJE INTERNACIONAL` chunks;
- the top result was still from the `nacional` document instead of the explicit
  `internacional` policy family.

This is a specific disambiguation issue between sibling policy variants, not a
general viajes-category onboarding failure.

## Scope

This slice should:

1. bias explicit `viaje internacional` policy intent toward the international
   clausulado family;
2. keep national-policy retrieval and broad viajes-policy retrieval stable;
3. reuse existing operator-curated normalization seams where possible.

This slice should not:

- redesign the whole viajes ranking stack;
- add broad guide-family logic unless separate evidence requires it;
- change the baseline onboarding artifacts already generated.

## Required Behavior

Acceptance criteria:

- explicit `internacional` policy queries prefer
  `CONDICIONADO SEGURO VIAJE INTERNACIONAL`;
- explicit `nacional` policy queries prefer
  `CONDICIONADO SEGURO VIAJE NACIONAL`;
- broad policy queries without a variant anchor remain free to retrieve both
  families;
- the gap is covered by focused regression tests and documented live evidence.
