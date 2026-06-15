# Requirements

## Title

Recover clausulado-family routing for bicicletas y patinetas coverage queries.

## Context

The acceptance matrix still leaves `MOVILIDAD/BICICLETAS Y PATINETAS` pending. The deductible smoke query already retrieves the intended `pv bicis y patinetas v2.pdf` evidence, but the coverage smoke query `¿Qué cubre el seguro para bicicletas y patinetas?` currently routes to `politicas de suscripcion de movilidad.pdf` instead of the expected clausulado family `clausulado-bicis y patinetas.pdf`.

The retrieval contract already supports operator-curated deterministic query filter rules. The narrowest corrective action is to pin explicit bicicletas/patinetas coverage queries to the normalized clausulado family.

## Scope

This slice should:

1. Add one deterministic `document_name` routing rule for explicit bicicletas/patinetas coverage queries.
2. Preserve the existing deductible retrieval behavior.
3. Add focused regressions for repository-loaded term equivalences.
4. Update roadmap and the acceptance matrix with the outcome.

This slice should not:

- redesign bicis/patinetas chunking;
- broaden to generic movilidad policy questions;
- alter the deductible-specific retrieval path.

## Required Behavior

### 1. Explicit coverage family routing

Acceptance criteria:

- a query that explicitly asks what the bicicletas/patinetas insurance covers normalizes to `document_name = SEGURO DE BICICLETA`;
- `product=movilidad` and `document_type=policy` remain preserved when already present;
- generic movilidad policy queries do not receive this clausulado-family filter.

### 2. Retrieval and answer alignment

Acceptance criteria:

- live retrieval for `¿Qué cubre el seguro para bicicletas y patinetas?` stays inside `clausulado-bicis y patinetas.pdf`;
- grounded answering cites that clausulado family rather than `politicas de suscripcion de movilidad.pdf`;
- the deductible query keeps `pv bicis y patinetas v2.pdf` as its primary evidence.

### 3. Regression safety

Acceptance criteria:

- focused tests cover the committed routing rule;
- existing deductible tests still pass;
- unrelated movilidad policies do not gain this document-name injection.
