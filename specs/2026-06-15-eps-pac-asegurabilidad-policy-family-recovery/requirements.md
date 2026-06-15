# Requirements

## Title

Recover `PAC 60 Más` asegurabilidad policy-family routing.

## Context

The first live P1 MVP acceptance pass on `2026-06-15` showed that the PAC row
still fails even though the relevant PAC policy artifacts are already onboarded.

Observed live failure:

- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product pac --document-type policy --top-k 5`
  returned `clausulado pac 60 mas sura v1.pdf` chunks instead of the intended
  `politicas asegurabilidad pac 60 mas.pdf` family.
- `answer-query` for the same prompt therefore grounded itself on clausulado
  chunks instead of the dedicated asegurabilidad policy family.

Root-cause hypothesis:

- the current PAC `60 mas` clausulado rule in `ops/term-equivalences.json`
  still matches broad `pac 60 mas` policy questions because its `any_of`
  contains the generic token `pac`;
- as a result, `normalize_retrieval_query_with_term_equivalences(...)` injects
  the clausulado `document_name` before the narrower asegurabilidad rule can
  apply.

## Scope

This slice should:

1. narrow the PAC `60 mas` clausulado routing so it only captures explicit
   coverage/clausulado intent;
2. preserve the dedicated asegurabilidad routing for
   `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?`;
3. add a regression check against the repository term-equivalence file so this
   operator-rule conflict cannot silently return.

This slice should not:

- change PAC ingestion artifacts;
- onboard new PAC documents;
- broaden PAC reranking beyond the narrow asegurabilidad-vs-clausulado fix;
- address the separate general-PAC (`v16`) policy family unless needed by the
  same narrow rule correction.

## Required Behavior

### 1. Narrow clausulado rule

Acceptance criteria:

- a PAC `60 mas` query without explicit coverage/clausulado language must not
  receive `document_name="Es tiempo devIvIr mas historias."` by default;
- explicit PAC coverage queries such as `¿Qué cubre el PAC 60 Más?` must still
  resolve to the clausulado family.

### 2. Preserve asegurabilidad routing

Acceptance criteria:

- `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` normalizes to
  `document_name="Plan Complementario 60 más"`;
- live retrieval for that query returns the `politicas asegurabilidad pac 60 mas.pdf`
  family first or near-first without clausulado-first drift;
- live grounded answering for that query stays inside the same family.

### 3. Documentation

Acceptance criteria:

- the roadmap records closure of this blocker if the live PAC validation passes;
- the MVP acceptance matrix updates the PAC status from `fail` only if both
  retrieval and grounded answer satisfy the intended family gate.
