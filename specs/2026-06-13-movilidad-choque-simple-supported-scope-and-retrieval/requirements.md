# Requirements

## Title

Add supported-scope and retrieval baseline for `choque simple` mobility queries.

## Context

`MOVILIDAD/TRANSVERSALES` now exists as a shared mobility corpus baseline.
Among those documents, `choque simple` is the clearest repeated intent family:

- `circular choque simple.pdf`
- `como tomar fotos choque simple v2.pdf`
- `ley 2251 de 2022 choque simple.pdf`
- `proceso atencion choque simple v2.pdf`
- `proceso recobro choque simple v2.pdf`

At the moment, the project does not yet provide a narrow supported query seam
for that family, and a generic retrieval query may drift toward unrelated
mobility documents.

## Scope

This slice should:

- admit `choque simple` questions into supported query scope;
- default those queries toward the shared `product=movilidad` corpus and
  `document_type=guide`;
- add a narrow curated expansion bundle so the transversal `choque simple`
  corpus can win retrieval over unrelated mobility documents.

This slice should not:

- introduce a new product taxonomy;
- add broader operational intents beyond `choque simple`;
- redesign retrieval ranking or chunking;
- introduce normative document subtypes yet.

## Acceptance Criteria

### 1. Supported scope

- Queries such as `¿Qué debo hacer en un choque simple?` classify as
  supported.

### 2. Retrieval defaults

- `choque simple` queries can default to `product=movilidad` and
  `document_type=guide` when the caller did not already provide filters.

### 3. Curated retrieval alignment

- The retrieval path can carry a narrow lexical bundle anchored on the
  `choque simple` corpus language, such as Article 16 / Ley 2251, evidence
  gathering, vehicle removal, conciliation, and police-report replacement.

### 4. Backward compatibility

- Focused query-scope and retrieval tests pass.
- Existing mobility and coverage retrieval behavior remains unchanged.
