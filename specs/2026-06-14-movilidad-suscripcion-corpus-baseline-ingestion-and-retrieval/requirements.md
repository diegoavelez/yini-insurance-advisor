# Requirements

## Title

Baseline-ingest the `suscripción` transversal mobility cohort and validate
first retrieval behavior.

## Context

The `MOVILIDAD/TRANSVERSALES` corpus has now completed four narrow,
validated onboarding sequences:

- `choque simple`
- `propuesta de valor movilidad`
- `utilitarios y pesados`
- `financiación`

The next smallest remaining transversal document is now
`politicas de suscripcion de movilidad.pdf`.

Unlike the prior financing slice, this cohort is already classified in the
current metadata overlays as:

- `document_type=policy`
- `product=movilidad`

This makes `suscripción` the next truthful single-document onboarding target
before broadening into any other shared mobility process material.

## Scope

This slice should:

1. ingest only the `suscripción` cohort;
2. generate embeddings and index only that cohort;
3. run first retrieval checks against the indexed cohort;
4. identify the next narrow corrective slice only if real retrieval evidence
   shows a gap.

This slice should not:

- broaden into other transversal documents;
- redesign taxonomy beyond the current shared `product=movilidad` baseline;
- introduce reranking or intent-alignment logic before observing a real miss;
- mix `suscripción` with `financiación`, `PV`, or `choque simple` validation.

## Required Behavior

### 1. Narrow cohort ingestion

Acceptance criteria:

- only `politicas de suscripcion de movilidad.pdf` is targeted by the cohort
  run;
- processed, cleaned-markdown, and chunk artifacts are generated for the
  document;
- persisted metadata remains truthful to the existing overlay:
  - `document_type=policy`
  - `product=movilidad`

### 2. Narrow cohort indexing

Acceptance criteria:

- embeddings are generated only for the cohort chunk artifact;
- Qdrant indexing targets only the cohort embedding artifact;
- manifest evidence shows successful processing or captures a concrete runtime
  blocker.

### 3. First retrieval validation

Acceptance criteria:

- at least one suscripción-oriented retrieval query is run;
- retrieved chunks belong to the expected suscripción document family or
  reveal a concrete ranking/scope gap;
- any follow-on issue is written as a new narrow corrective slice rather than
  fixed ad hoc.

### 4. Documentation and roadmap

Acceptance criteria:

- the roadmap remains consistent with this slice as the next operational
  transversal cohort;
- the spec bundle includes the exact cohort commands to run.
