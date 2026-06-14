# Requirements

## Title

Align supported scope and retrieval for suscripción `facturación por asegurado` queries.

## Context

A post-remediation live validation battery over `politicas de suscripcion de movilidad`
exposed a new narrow gap:

- the query `¿Qué condiciones aplican a la facturación por asegurado en pólizas colectivas?`
  currently returns an unsupported-scope refusal even though the answer is present
  in the suscripción corpus under the collective billing material;
- live retrieval for that query can surface the suscripción family, but the exact
  chunk that contains the `Facturación por asegurado` conditions is not reliably
  prioritized.

This is now a narrow supported-scope plus retrieval-intent alignment problem for
one documented suscripción query pattern.

## Scope

This slice should:

1. admit `facturación por asegurado` suscripción queries into supported scope;
2. prefer the chunk that contains the documented `Facturación por asegurado`
   conditions inside the suscripción collective billing material;
3. keep the fix deterministic and narrowly scoped to this query pattern.

This slice should not:

- redesign the global supported-scope classifier;
- reopen markdown normalization for the suscripción PDF;
- broaden into generic ranking changes for all `asegurado` queries.

## Required Behavior

### 1. Supported-scope admission

Acceptance criteria:

- representative Spanish suscripción questions about `facturación por asegurado`
  are classified as supported;
- the typed supported/unsupported contract remains unchanged.

### 2. Retrieval alignment

Acceptance criteria:

- explicit `facturación por asegurado` suscripción queries prioritize the chunk
  that contains the documented conditions for that modality;
- retrieval remains inside the suscripción document family under the existing
  movilidad policy scope.

### 3. Live answer recovery

Acceptance criteria:

- at least one live `answer-query` run for
  `¿Qué condiciones aplican a la facturación por asegurado en pólizas colectivas?`
  returns `supported=true`;
- the grounded answer cites suscripción evidence rather than refusing for scope.
