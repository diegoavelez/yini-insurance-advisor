# Requirements

## Title

Bring `MOVILIDAD/SOAT` into the current RAG baseline.

## Context

Two new `SOAT` source PDFs now exist under `data/raw/MOVILIDAD/SOAT`:

- `clausulado soat.pdf`
- `tarifas soat 2026.pdf`

The current repository has no canonical `soat` product taxonomy, no overlays
for these documents, and no explicit supported-scope coverage for `SOAT`
queries. The next narrow slice should add the minimum truthful baseline needed
to ingest and retrieve this category.

## Scope

This slice should:

1. Add canonical `soat` query and filter aliases.
2. Add minimal supported-scope admission for `SOAT` queries.
3. Add curated overlay metadata for the two source PDFs.
4. Ensure path-derived product inference can resolve `product=soat`.
5. Record the baseline slice in the roadmap.

This slice should not:

- redesign document-type taxonomy;
- implement tariff-specific reranking or date-sensitive retrieval tuning;
- run comparative or deep corrective work before real evidence exists.

## Required Behavior

### 1. SOAT taxonomy baseline

Acceptance criteria:

- `soat` is a canonical retrieval-facing `product` value;
- queries mentioning `SOAT` or common full-form aliases normalize toward that
  canonical value;
- metadata filter aliases can resolve `soat`.

### 2. Supported query scope

Acceptance criteria:

- representative SOAT queries such as `¿Cuáles son las tarifas del SOAT 2026?`
  classify as supported.

### 3. Overlay baseline

Acceptance criteria:

- `clausulado soat` persists as `document_type=policy` and `product=soat`;
- `tarifas soat 2026` persists as `document_type=guide` and `product=soat`.

### 4. Backward compatibility

Acceptance criteria:

- focused query-scope and ingestion tests pass;
- existing category behavior remains unchanged.
