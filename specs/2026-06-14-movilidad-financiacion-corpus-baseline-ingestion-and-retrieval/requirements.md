# Requirements

## Title

Baseline-ingest the `financiación` transversal mobility cohort and validate
first retrieval behavior.

## Context

The `MOVILIDAD/TRANSVERSALES` corpus has now completed three narrow,
validated intent families:

- `choque simple`
- `propuesta de valor movilidad`
- `utilitarios y pesados`

The next smallest unprocessed transversal document is now
`instructivo financiacion de polizas v1.pdf`.

Unlike the previous `utilitarios y pesados` pair, this is a one-document
cohort already covered by the current metadata overlays as:

- `document_type=guide`
- `product=movilidad`

This makes `financiación` the narrowest truthful next onboarding target
before broader or more policy-heavy materials such as `suscripción`.

## Scope

This slice should:

1. Ingest only the `financiación` cohort.
2. Generate embeddings and index only that cohort.
3. Run first retrieval checks against the indexed cohort.
4. Identify the next narrow corrective slice only if real retrieval evidence
   shows a gap.

This slice should not:

- broaden into `suscripción`;
- redesign taxonomy beyond the current shared `product=movilidad` baseline;
- introduce new reranking logic before observing a real miss;
- bundle unrelated transversal documents into the same run.

## Required Behavior

### 1. Narrow cohort ingestion

Acceptance criteria:

- only `instructivo financiacion de polizas v1.pdf` is targeted by the cohort
  run;
- processed, cleaned-markdown, and chunk artifacts are generated for the
  document;
- persisted metadata remains truthful to the existing overlay:
  - `document_type=guide`
  - `product=movilidad`

### 2. Narrow cohort indexing

Acceptance criteria:

- embeddings are generated only for the cohort chunk artifact;
- Qdrant indexing targets only the cohort embedding artifact;
- manifest evidence shows successful processing or captures a concrete runtime
  blocker.

### 3. First retrieval validation

Acceptance criteria:

- at least one financing-oriented retrieval query is run;
- retrieved chunks belong to the expected financing document family or reveal a
  concrete ranking/scope gap;
- any follow-on issue is written as a new narrow corrective slice rather than
  fixed ad hoc.

### 4. Documentation and roadmap

Acceptance criteria:

- the new slice is recorded in the roadmap as the next operational transversal
  cohort;
- the spec bundle includes the exact cohort commands to run.
