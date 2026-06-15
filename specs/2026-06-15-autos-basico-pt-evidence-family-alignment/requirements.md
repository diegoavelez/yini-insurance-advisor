# Requirements

## Title

Align explicit `Autos Básico PT` coverage queries to the intended guide-family evidence.

## Context

`MOVILIDAD/AUTOS` currently fails the MVP acceptance matrix because the grounded-answer smoke query `¿Qué cubre el plan autos básico PT?` retrieves and cites unrelated guide families such as `ayudaventas autos electricos e hibridos.pdf` and `diferenciales planes autos.pdf` ahead of, or alongside, the intended `generalidades plan autos basico pt v2.pdf` family.

The retrieval contract already supports operator-curated deterministic query filter rules in `ops/term-equivalences.json`. The narrowest corrective action is to route explicit `Autos Básico PT` intent to the specific document family that actually names that plan.

## Scope

This slice should:

1. Add one deterministic operator-curated `document_name` rule for explicit `Autos Básico PT` guide queries.
2. Add one narrow coverage-oriented query-expansion rule so the explicit `Coberturas principales` table can compete inside that same family.
3. Keep the existing AUTOS comparison retrieval behavior unchanged.
4. Add regression coverage for repository-loaded term equivalences.
5. Record the partial remediation in the roadmap and MVP matrix.

This slice should not:

- redesign AUTOS comparison reranking;
- change the retrieval or answer contracts;
- add probabilistic plan classification;
- broaden the rule to generic autos coverage queries.

## Required Behavior

### 1. Explicit `Autos Básico PT` family routing

When a query explicitly names `Autos Básico PT` (or its equivalent full plan wording), retrieval should inject the intended guide-family `document_name` filter.

Acceptance criteria:

- queries that explicitly mention `autos` plus `básico pt` or the full plan wording normalize to `document_name = Plan Autos Básico Pérdidas Totales`;
- the rule preserves `product=auto` and `document_type=guide` when those filters are already present;
- generic AUTOS coverage queries without the explicit `Básico PT` anchor do not receive this family filter.

### 2. Regression safety

Acceptance criteria:

- explicit `Autos Básico PT` coverage queries append narrow coverage terms such as the plan's main coverage labels;
- that expansion increases candidate-pool breadth only for the explicit plan-specific coverage path;
- repository-backed normalization tests cover the committed rule;
- existing PAC and SOAT rule tests remain valid;
- AUTOS comparison queries continue to avoid this document-family injection.

### 3. Documentation traceability

Acceptance criteria:

- the roadmap records the corrective slice;
- the MVP matrix notes that `Autos Básico PT` family alignment is fixed, while any remaining AUTOS comparison-ranking gap stays explicit.
