# Requirements

## Title

Normalize diagrammatic `pv` blocks for `MOVILIDAD/BICICLETAS Y PATINETAS` into semantically richer chunk inputs.

## Context

The `pv bicis y patinetas v2.pdf` document is now ingested and retrievable, but
its most valuable sections still arrive as page-number headings plus line-broken
diagram blocks. Unlike the previous AUTOS comparison document, this file does
not reach the pipeline as markdown tables, so the current table normalization
path does not activate.

The next narrow slice should improve chunk semantics before retrieval by:

1. avoiding `Page N` as the dominant section label when a stronger semantic
   heading is present inside the block;
2. skipping trivial emitted page-heading blocks;
3. rewriting the line-grid `COBERTURAS Y PLANES` content into deterministic
   statement-style text.

## Scope

This slice should:

- keep the existing chunk, embedding, and retrieval contracts unchanged;
- add narrow deterministic normalization for the current diagrammatic `pv`
  pattern;
- preserve backward compatibility for ordinary paragraph and markdown-table
  inputs.

This slice should not:

- introduce LLM summarization;
- redesign the whole chunking pipeline;
- hardcode a source document id;
- change Qdrant or answer-generation interfaces.

## Acceptance Criteria

- `Page N` headings do not become standalone trivial chunk content.
- A block containing a stronger semantic label such as `COBERTURAS Y PLANES`,
  `GENERALIDADES`, `EXPEDICIÓN REQUISITOS`, `DEDUCIBLE`, or
  `PROPUESTA DE VALOR` uses that label as section context.
- The `COBERTURAS Y PLANES` line-grid is rewritten into more semantic
  statement-style lines.
- Focused ingestion tests pass and existing non-insurance scope behavior
  remains unchanged.
