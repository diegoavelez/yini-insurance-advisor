# Requirements

## Title

Recover direct asegurabilidad section priority for `PAC 60 Más` answers.

## Context

`EPS/PAC` is currently marked `fragile-pass` in the MVP matrix. The prior corrective slice fixed the document-family drift for `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?`, but live retrieval still ranks unrelated in-family sections such as `CONGELACIONES` and `REACTIVACIÓN` above the direct asegurabilidad sections `GRUPOS ASEGURABLES` and the age / affiliation requirements.

The retrieval contract already supports operator-curated query expansion. The narrowest next step is to enrich explicit `PAC 60 Más` asegurabilidad queries with the section anchors that actually contain the intended answer.

## Scope

This slice should:

1. Add one operator-curated expansion rule for explicit `PAC 60 Más` asegurabilidad queries.
2. Reuse the existing hybrid candidate-pool and reranking seam.
3. Add focused regressions for the explicit asegurabilidad path.
4. Update roadmap and MVP matrix with the new outcome.

This slice should not:

- change the PAC document-family routing already in place;
- introduce PAC-specific retrieval-core branching if the curated rule is sufficient;
- broaden to generic PAC policy questions.

## Required Behavior

### 1. PAC 60 Más asegurabilidad section anchors

When a query explicitly asks for `PAC 60 Más` asegurabilidad conditions, retrieval should append canonical section anchors aligned with the answer-bearing chunks.

Acceptance criteria:

- `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` matches one committed expansion rule;
- the appended terms include anchors such as `grupos asegurables`, age/admission requirements, and collective-threshold wording;
- the original query remains intact.

### 2. In-family section prioritization

Acceptance criteria:

- the matched rule expands the candidate pool beyond bare `top_k`;
- deterministic reranking lifts `GRUPOS ASEGURABLES` and direct ingreso/requisitos chunks above `CONGELACIONES` and `REACTIVACIÓN` for the explicit query;
- the answer-facing citations become tighter and more representative of the direct asegurabilidad content.

### 3. Regression safety

Acceptance criteria:

- focused tests cover expansion and reranking for the explicit `PAC 60 Más` asegurabilidad query;
- the explicit `PAC 60 Más` family routing still holds;
- unrelated PAC clauses and forms do not gain this expansion bundle.
