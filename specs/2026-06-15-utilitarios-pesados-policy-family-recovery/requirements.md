# Requirements

## Title

Recover the policy family for explicit utilitarios y pesados coverage queries.

## Context

The MVP acceptance row for `MOVILIDAD/UTILITARIO Y PESADOS` remains pending. The guide smoke query already retrieves the intended `ayudaventas utilitarios y pesados v2.pdf` family. The remaining gap is the grounded-answer smoke query `¿Qué cubre el plan de utilitarios y pesados?`, which currently falls back to `politicas de suscripcion de movilidad.pdf` instead of the dedicated clausulado family `clausulado-plan utilitarios y pesados.pdf`.

## Scope

This slice should:

1. Add one deterministic `document_name` routing rule for explicit utilitarios y pesados coverage queries.
2. Preserve the existing guide-family routing for benefits and assistance queries.
3. Add focused regressions for repository-loaded equivalences and retrieval filtering.
4. Update roadmap and the acceptance matrix after live validation.

This slice should not:

- redesign utilitarios chunking;
- broaden to generic movilidad policy queries;
- alter the existing guide-family behavior.

## Required Behavior

### 1. Explicit policy-family routing

Acceptance criteria:

- a query that explicitly asks what the utilitarios y pesados plan covers normalizes to `document_name = SEGURO DE AUTOS PLAN UTILITARIOS Y PESADOS`;
- the rule can overwrite a broad `product=movilidad` filter into the narrower product family when the query clearly targets utilitarios y pesados;
- guide-oriented benefit queries keep the existing `Seguro de Autos Utilitarios y Pesados` guide family.

### 2. Retrieval and answer alignment

Acceptance criteria:

- live grounded answering for `¿Qué cubre el plan de utilitarios y pesados?` stays inside `clausulado-plan utilitarios y pesados.pdf`;
- the answer cites real `Coberturas` sections instead of the transversal suscripción policy document.

### 3. Regression safety

Acceptance criteria:

- focused tests cover the new policy-family routing rule;
- existing utilitarios guide tests still pass.
