# Requirements

## Title

Constrain explicit `utilitarios y pesados` guide-intent retrieval to the
cohort guide family.

## Context

The baseline `utilitarios y pesados` cohort onboarding is now complete for the
two intended documents:

- `ayudaventas utilitarios y pesados v2.pdf`
- `clausulado-plan utilitarios y pesados.pdf`

Live validation produced two distinct outcomes:

- the policy-oriented query `qué cubre el plan de utilitarios y pesados`
  correctly retrieved only `SEGURO DE AUTOS PLAN UTILITARIOS Y PESADOS`
  policy chunks;
- the guide-oriented query
  `qué beneficios o asistencias tienen los utilitarios y pesados`
  retrieved generic `PROPUESTA DE VALOR MOVILIDAD` chunks ahead of the
  cohort-specific `Seguro de Autos Utilitarios y Pesados` guide.

This is now a concrete ranking/scope gap, not a hypothetical one. The next
narrow corrective slice should constrain this explicit guide-family intent
through the existing operator-curated filter seam, without changing taxonomy or
introducing a broader reranker redesign.

## Scope

This slice should:

1. Add a narrow operator-curated filter rule for explicit
   `utilitarios y pesados` guide-intent queries.
2. Constrain retrieval to the `Seguro de Autos Utilitarios y Pesados`
   document family when that rule matches.
3. Keep policy retrieval and broader movilidad guide retrieval unchanged.

This slice should not:

- redesign the global movilidad taxonomy;
- change `policy` retrieval behavior for the cohort;
- introduce new retrieval payload fields;
- add ad hoc hardcoded source-PDF checks in reranking code.

## Required Behavior

### 1. Explicit guide-family scoping

When a query explicitly asks about benefits, assistance, or commercial value
for `utilitarios y pesados`, retrieval should default to the cohort guide
family rather than generic movilidad PV material.

Acceptance criteria:

- the query matches a curated `query_filter_rule` that sets
  `document_name = Seguro de Autos Utilitarios y Pesados`;
- the rule requires both the cohort anchor (`utilitarios y pesados`) and
  guide-intent language such as `beneficios`, `asistencias`, or comparable
  commercial-guide wording;
- explicit caller-provided `document_name` filters still take precedence.

### 2. Retrieval-family alignment

The existing retrieval pipeline should reuse the new filter for both semantic
retrieval and local lexical recall.

Acceptance criteria:

- normalized retrieval queries carry the cohort guide `document_name` filter
  when the rule matches;
- Qdrant query filters include that `document_name` constraint;
- local lexical candidates from generic movilidad guides such as
  `PROPUESTA DE VALOR MOVILIDAD` are excluded by the same rule.

### 3. Backward compatibility

Existing behavior outside this narrow scenario should remain stable.

Acceptance criteria:

- current retrieval tests still pass;
- the policy-oriented `utilitarios y pesados` query path remains unchanged;
- non-cohort movilidad guide queries do not inherit the new filter.

### 4. Documentation and roadmap

The roadmap should record that the baseline cohort onboarding is complete and
that the remaining issue is a narrow guide-family ranking correction.

Acceptance criteria:

- the new slice is listed in the roadmap;
- the prior baseline cohort slice is no longer marked as remaining;
- the implementation note describes the gap using the observed live retrieval.
