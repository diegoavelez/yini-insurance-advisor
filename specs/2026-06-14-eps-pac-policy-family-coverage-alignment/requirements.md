# Requirements

## Title

Onboard and align the general `EPS/PLAN COMPLEMENTARIO PAC` asegurabilidad
policy family.

## Context

After the completed `PAC 60+ core`, `formularios / gestión básica`,
`Global Web`, and long instructivos cohorts, the next narrow PAC slice is the
general asegurabilidad policy follow-on:

- `politicas asegurabilidad pac v16.pdf`

This slice is the correct next step because:

- it is the remaining semantically narrow PAC policy document before the two
  large isolated PDFs;
- current PAC `60+` query-filter rules are broad enough to capture general PAC
  asegurabilidad intents incorrectly;
- onboarding the general PAC asegurabilidad document provides the right anchor
  for policy-intent retrieval without requiring the heavy general clausulado
  PDF yet.

## Scope

This slice should:

1. add canonical metadata support for `politicas asegurabilidad pac v16.pdf`
   under `product=pac`, `document_type=policy`;
2. onboard the document through ingestion, embeddings, and Qdrant indexing;
3. narrow the existing `PAC 60+` asegurabilidad query-filter routing so it does
   not hijack general PAC asegurabilidad queries;
4. align general PAC asegurabilidad queries to the onboarded `v16` family.

This slice should not:

- onboard `clausulado pac tradicional sura v1.pdf`;
- onboard `informacion canales transaccionales y apoyo v1.pdf`;
- reopen `PAC 60+`, PAC forms, `Global Web`, or long instructivos;
- introduce broad PAC reranking beyond the narrow asegurabilidad-family fix.

## Required Behavior

### 1. Canonical metadata support

Acceptance criteria:

- `politicas asegurabilidad pac v16.pdf` persists with canonical `product=pac`;
- overlay-backed metadata persists it as `document_type=policy`.

### 2. Narrow PAC family routing

Acceptance criteria:

- `PAC 60+` asegurabilidad routing requires explicit `60 Más` wording (or its
  normalized equivalent) rather than any generic `pac` asegurabilidad query;
- a general PAC asegurabilidad query can route to the general PAC policy family
  without being captured by `PAC 60+`.

### 3. Retrieval validation

Acceptance criteria:

- `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` stays in the
  `PAC 60+` asegurabilidad family;
- `¿Qué condiciones de asegurabilidad tiene el plan complementario PAC?`
  retrieves the new `politicas asegurabilidad pac v16.pdf` family first;
- if any deterministic routing is required, it remains narrowly scoped to
  asegurabilidad intents only.

### 4. Documentation and roadmap

Acceptance criteria:

- the roadmap reflects that PAC policy follow-on is completed after this
  slice;
- the validation file records the remaining deferred PAC large isolated PDFs.
