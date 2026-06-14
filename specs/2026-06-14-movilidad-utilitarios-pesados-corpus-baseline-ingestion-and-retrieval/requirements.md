# Requirements

## Title

Baseline-ingest the `utilitarios y pesados` transversal mobility cohort and
validate first retrieval behavior.

## Context

The `MOVILIDAD/TRANSVERSALES` corpus now has two successfully validated intent
families:

- `choque simple`
- `propuesta de valor movilidad`

The next coherent cohort identified during the transversal review is
`utilitarios y pesados`, represented by:

- `ayudaventas utilitarios y pesados v2.pdf`
- `clausulado-plan utilitarios y pesados.pdf`

These two files form a small commercial+contractual pair, which makes them a
better next onboarding target than broader operational documents such as
`financiación` or `suscripción`.

The next narrow slice should run the smallest truthful baseline for this cohort:
ingestion, embeddings, indexing, and first retrieval validation under the
current shared `product=movilidad` taxonomy.

## Scope

This slice should:

1. Ingest only the `utilitarios y pesados` cohort.
2. Generate embeddings and index only that cohort.
3. Run first retrieval checks against the indexed cohort.
4. Identify the next narrow corrective slice only if real retrieval evidence
   shows a gap.

This slice should not:

- broaden into `financiación` documents;
- broaden into `suscripción` documents;
- redesign taxonomy beyond the current `product=movilidad` baseline;
- preemptively add reranking logic before observing a real miss.

## Required Behavior

### 1. Narrow cohort ingestion

Acceptance criteria:

- only the two `utilitarios y pesados` PDFs are targeted by the cohort run;
- processed, cleaned-markdown, and chunk artifacts are generated for both;
- persisted metadata remains truthful to the existing overlays:
  - `ayudaventas ...` as `guide`
  - `clausulado-plan ...` as `policy`
  - both under `product=movilidad`

### 2. Narrow cohort indexing

Acceptance criteria:

- embeddings are generated only for the cohort chunk artifacts;
- Qdrant indexing targets only the cohort embedding artifacts;
- manifest evidence shows successful processing for both documents or captures a
  concrete runtime blocker.

### 3. First retrieval validation

Acceptance criteria:

- at least one guide-oriented query and one policy-oriented query are run;
- retrieved chunks belong to the expected cohort or reveal a concrete ranking/scope gap;
- any follow-on issue is written as a new narrow corrective slice rather than
  fixed ad hoc.

### 4. Documentation and roadmap

Acceptance criteria:

- the new slice is recorded in the roadmap as the next operational cohort;
- the spec bundle includes the exact cohort commands to run.
