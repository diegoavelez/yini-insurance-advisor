# Requirements

## Title

Onboard and align the isolated `EPS/PLAN COMPLEMENTARIO PAC` traditional
clausulado policy.

## Context

After the completed `PAC 60+ core`, `formularios / gestión básica`,
`Global Web`, long instructivos, and PAC policy follow-on slices, the next
truthful PAC slice is the isolated traditional clausulado:

- `clausulado pac tradicional sura v1.pdf`

This slice is the correct next step because:

- it is the highest-value remaining PAC isolated PDF for policy coverage
  retrieval;
- current broad PAC clausulado routing still points to the `PAC 60+`
  clausulado family;
- onboarding the traditional clausulado should become the correct anchor for
  generic PAC coverage/clausulado queries, while explicit `60 Más` queries
  remain in the `PAC 60+` family.

## Scope

This slice should:

1. add canonical metadata support for `clausulado pac tradicional sura v1.pdf`
   under `product=pac`, `document_type=policy`;
2. onboard the document through ingestion, embeddings, and Qdrant indexing;
3. narrow the existing `PAC 60+` clausulado routing so it requires explicit
   `60 Más` wording;
4. align generic PAC coverage/clausulado queries to the traditional clausulado
   family.

This slice should not:

- onboard `informacion canales transaccionales y apoyo v1.pdf`;
- reopen `PAC 60+`, PAC forms, `Global Web`, long instructivos, or PAC policy
  follow-on;
- introduce broad PAC reranking unrelated to clausulado-family disambiguation.

## Required Behavior

### 1. Canonical metadata support

Acceptance criteria:

- `clausulado pac tradicional sura v1.pdf` persists with canonical
  `product=pac`;
- overlay-backed metadata persists it as `document_type=policy`.

### 2. Narrow PAC clausulado routing

Acceptance criteria:

- `PAC 60+` clausulado routing requires explicit `60 Más` wording (or its
  normalized equivalent) rather than any generic `pac` coverage query;
- a general PAC coverage/clausulado query can route to the traditional
  clausulado family without being captured by `PAC 60+`.

### 3. Retrieval validation

Acceptance criteria:

- `¿Qué cubre el PAC 60 Más?` stays in the `PAC 60+` clausulado family;
- `¿Qué cubre el plan complementario PAC?` retrieves the traditional
  clausulado family first;
- `¿Qué cubre el clausulado del plan complementario PAC?` also retrieves the
  traditional clausulado family first.

### 4. Documentation and roadmap

Acceptance criteria:

- the roadmap reflects that only the last isolated PAC PDF remains after this
  slice;
- the validation file records `informacion canales transaccionales y apoyo
  v1.pdf` as the only remaining PAC large isolated PDF.
