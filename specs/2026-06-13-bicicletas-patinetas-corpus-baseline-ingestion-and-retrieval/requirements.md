# Requirements

## Title

Bring `MOVILIDAD/BICICLETAS Y PATINETAS` into the current RAG baseline.

## Context

The next adjacent category after AUTOS is `MOVILIDAD/BICICLETAS Y PATINETAS`, which already has three source PDFs in `data/raw` but is not yet represented in the processed corpus. The RAG pipeline now has stronger metadata persistence, comparison retrieval hardening, and deterministic ingestion seams that should generalize to this neighboring mobility category.

The next narrow slice should add the minimum taxonomy and ingestion alignment needed to ingest, embed, index, and retrieve this category under the current product taxonomy.

## Scope

This slice should:

1. Add minimal query/filter alias support for bicycles and scooters under the existing `movilidad` product taxonomy.
2. Add minimal document-type alias support for `pv` artifacts if needed.
3. Ingest the three `BICICLETAS Y PATINETAS` PDFs.
4. Generate embeddings and index them into Qdrant.
5. Validate a few real retrieval queries.

This slice should not:

- introduce a new product taxonomy value distinct from `movilidad`;
- redesign UI filter surfaces;
- add comparison-specific reranking for this category unless evidence requires it.

## Required Behavior

### 1. Mobility alias alignment

Acceptance criteria:

- queries mentioning `bici`, `bicicleta`, `patineta`, or close plural variants can normalize toward the current `movilidad` product family;
- product-filter alias handling remains backward compatible for existing `movilidad` queries.

### 2. Baseline document-type persistence

Acceptance criteria:

- `clausulado` persists as `policy`;
- `ayudaventas` and `pv` persist as `guide` when no overlay overrides them.

### 3. Corpus onboarding

Acceptance criteria:

- the three source PDFs produce processed-document, chunk, embedding, and indexed artifacts without breaking existing categories;
- retrieval with `product=movilidad` can surface relevant chunks from this category.

### 4. Backward compatibility

Acceptance criteria:

- focused ingestion/retrieval tests pass;
- roadmap records the slice.
