# Requirements

## Title

Bring `MOVILIDAD/MOTOS` into the current RAG baseline.

## Context

The next adjacent mobility category is `MOVILIDAD/MOTOS`, which now exists in
`data/raw` with four source PDFs but is not yet represented in the processed
corpus. The repository already supports canonical `moto` scope/filter aliases,
path-derived product inference, curated overlays, and category-specific
corrective follow-ups when needed.

The next narrow slice should add the minimum metadata and document-type
alignment needed to ingest, embed, index, and retrieve this category under the
current taxonomy.

## Scope

This slice should:

1. Add curated overlay metadata for the four `MOTOS` source PDFs.
2. Ensure `comparativo` source paths can persist as `guide`.
3. Record the new category baseline in the roadmap.
4. Add focused ingestion regression coverage for the new document-type path.

This slice should not:

- add comparison-specific reranking for motorcycles yet;
- redesign supported query scope;
- broaden retrieval heuristics before real evidence shows a ranking gap.

## Required Behavior

### 1. MOTOS overlay baseline

Acceptance criteria:

- `ayudaventas asistencia pequeños eventos motos` persists as `guide` and
  `product=moto`;
- `ayudaventas motos v2` persists as `guide` and `product=moto`;
- `clausulado-plan motos` persists as `policy` and `product=moto`;
- `comparativo motos` persists as `guide` and `product=moto`.

### 2. Baseline document-type inference

Acceptance criteria:

- a `comparativo motos.pdf` source path can infer `document_type=guide` when no
  overlay is provided;
- existing `guide` path inference for `ayudaventas`, `diferenciales`, and `pv`
  remains backward compatible.

### 3. Backward compatibility

Acceptance criteria:

- focused ingestion tests pass;
- the roadmap records the slice without reopening older phases.
