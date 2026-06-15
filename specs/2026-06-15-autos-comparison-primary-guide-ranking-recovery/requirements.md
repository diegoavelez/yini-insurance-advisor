# Requirements

## Title

Recover the primary `DIFERENCIALES SURA` guide ranking for broad AUTOS comparison queries.

## Context

The MVP acceptance matrix still fails `MOVILIDAD/AUTOS` because the broad comparison smoke query `¿Qué diferencia hay entre los planes de autos?` ranks unrelated electric/hybrid AUTOS guide evidence above the intended comparative guide family `diferenciales planes autos.pdf`.

Previous AUTOS comparison slices improved comparison retrieval for narrower prompts that explicitly mention `plan básico` and `otros planes`, but the broader smoke query does not currently trigger those operator-curated expansion rules.

## Scope

This slice should:

1. Add one operator-curated broad AUTOS comparison expansion rule.
2. Reuse the existing hybrid candidate-pool and reranking seam.
3. Add focused regressions for the broad query path.
4. Update roadmap and MVP matrix with the new outcome.

This slice should not:

- introduce new retrieval contracts;
- add LLM-based query rewriting;
- add AUTOS-only imperative logic in the retrieval core if the curated rule is sufficient;
- change the explicit `Autos Básico PT` coverage routing added in the prior slice.

## Required Behavior

### 1. Broad AUTOS comparison expansion

When a query broadly asks for differences between AUTOS plans, retrieval should append canonical comparison terms aligned with `DIFERENCIALES SURA`.

Acceptance criteria:

- a query such as `¿Qué diferencia hay entre los planes de autos?` matches one committed operator-curated expansion rule;
- the appended terms include the comparative document anchors used by the AUTOS comparison corpus;
- the query remains otherwise unchanged.

### 2. Candidate-pool and reranking reuse

Acceptance criteria:

- the matched rule expands the candidate pool via the existing comparison retrieval seam;
- deterministic reranking prefers the primary `DIFERENCIALES SURA` chunks over unrelated electric/hybrid marketing chunks for the broad query;
- existing narrower AUTOS comparison behavior remains valid.

### 3. Regression safety

Acceptance criteria:

- focused tests cover the broad AUTOS comparison query path;
- existing comparison and `Autos Básico PT` tests still pass;
- no unrelated products gain the AUTOS comparison bundle.
