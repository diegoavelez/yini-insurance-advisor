# Requirements

## Title

Normalize the linear `EXPEDICIÓN REQUISITOS` and `DEDUCIBLE` grids in the
`pv` document for `MOVILIDAD/BICICLETAS Y PATINETAS`.

## Context

The previous corrective slice promoted semantic section labels and normalized
`COBERTURAS Y PLANES`, but the `pv` document still contains two large
line-broken grids that remain difficult for embeddings and retrieval:

- `EXPEDICIÓN REQUISITOS`
- `DEDUCIBLE`

These sections are not markdown tables. They arrive as stacked line fragments
that should be rewritten into deterministic statement-style text while keeping
the current chunk and retrieval contracts intact.

## Scope

This slice should:

1. Rewrite the `EXPEDICIÓN REQUISITOS` grid into clearer product/range-based
   statements.
2. Rewrite the `DEDUCIBLE` grid into clearer product/range-based statements.
3. Preserve existing section promotion and chunk contracts.

This slice should not:

- introduce LLM summarization;
- redesign the full ingestion architecture;
- change embedding or retrieval interfaces.

## Acceptance Criteria

- `EXPEDICIÓN REQUISITOS` chunks contain deterministic statement-style lines
  instead of mostly fragmented line stacks.
- `DEDUCIBLE` chunks contain deterministic statement-style lines instead of
  mostly fragmented line stacks.
- Existing ingestion regressions continue to pass.
