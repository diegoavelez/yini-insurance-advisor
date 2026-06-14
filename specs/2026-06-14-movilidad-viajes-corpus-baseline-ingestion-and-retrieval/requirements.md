# Requirements

## Title

Baseline-ingest the `MOVILIDAD/VIAJES` category and validate first retrieval
behavior.

## Context

The raw movilidad corpus now includes a dedicated `VIAJES` folder with four
documents:

- `ayudaventas viaje ingles v2.pdf`
- `ayudaventas viajes español v2.pdf`
- `clausulado viaje internacional v1.pdf`
- `clausulado viaje nacional v1.pdf`

This category has not yet been onboarded into the canonical ingestion,
embedding, indexing, and retrieval path. The next truthful slice is the narrow
baseline onboarding of this folder as its own canonical product `viajes`.

## Scope

This slice should:

1. add canonical metadata support for the `VIAJES` category;
2. ingest only the four `VIAJES` PDFs;
3. generate embeddings and index only the resulting `VIAJES` artifacts;
4. run first retrieval checks for one guide-oriented and one policy-oriented
   query.

This slice should not:

- redesign retrieval ranking for `VIAJES` before observing a real miss;
- introduce document-family hardcoded reranking without evidence;
- broaden into non-`VIAJES` movilidad folders.

## Required Behavior

### 1. Canonical metadata support

Acceptance criteria:

- path-derived product inference resolves `MOVILIDAD/VIAJES/` to the canonical
  product `viajes`;
- overlay-backed metadata persists:
  - both `ayudaventas` PDFs as `guide`
  - both `clausulado` PDFs as `policy`;
- supported-scope admission recognizes direct `viajes` insurance queries.

### 2. Narrow category ingestion

Acceptance criteria:

- only the four `VIAJES` PDFs are targeted by the onboarding run;
- processed, cleaned-markdown, and chunk artifacts are generated for each;
- artifact ids persist under `movilidad__viajes__...`.

### 3. Narrow indexing and retrieval validation

Acceptance criteria:

- embeddings and Qdrant indexing target only the `VIAJES` artifacts;
- at least one guide query and one policy query succeed against the canonical
  `product=viajes` scope;
- any observed ranking/quality issue is recorded as a new narrow corrective
  slice rather than fixed ad hoc.

### 4. Documentation and roadmap

Acceptance criteria:

- the new slice is listed in the roadmap and category rollup;
- the spec bundle records the exact operator commands used for onboarding.
