# Requirements

## Title

Align `Muévete Libre` coverage-intent retrieval with the existing policy corpus.

## Context

`MOVILIDAD/MUEVETE LIBRE/clausulado muevete libre v2.pdf` now ingests correctly
through Docling and preserves semantically useful coverage sections such as
`1.1. Cobertura`, `1.2. Cobertura a la moto`, and the broader coverage
sections under `PLAN MUÉVETE LIBRE`.

Runtime validation shows the remaining gap is no longer ingestion-time
normalization. The current retrieval path still lets generic or adjacent policy
sections such as `Glosario`, `Prima`, or introductory material outrank the
actual coverage sections for a query such as `¿Qué cubre Muévete Libre?`.

The next narrow slice should correct that retrieval bias without redesigning
the retrieval pipeline.

## Scope

This slice should:

- keep chunk, embedding, and answer contracts unchanged;
- add narrow operator-curated query expansion for `Muévete Libre`
  coverage-intent queries;
- default those coverage-intent queries toward `document_type=policy` when the
  caller did not already specify a document type;
- add deterministic retrieval preference for chunks whose label surface
  explicitly contains `cobertura`.

This slice should not:

- rework the PDF-to-markdown conversion again;
- introduce model-based reranking;
- change Qdrant payload schemas;
- generalize a broad product-classifier beyond the current curated surface.

## Acceptance Criteria

### 1. Coverage-intent filter alignment

- Queries such as `¿Qué cubre Muévete Libre?` can default to
  `document_type=policy` when no explicit `document_type` filter was provided.

### 2. Coverage-intent retrieval expansion

- `Muévete Libre` coverage-intent queries can carry curated lexical anchors
  tied to the policy coverage sections.
- The retrieval candidate pool can surface plausible coverage chunks even when
  pure semantic similarity initially favors adjacent generic sections.

### 3. Deterministic coverage preference

- When a coverage-intent query is active, chunks with label surfaces that
  explicitly contain `cobertura` receive a deterministic preference over
  adjacent non-coverage sections.

### 4. Backward compatibility

- Focused retrieval and query-normalization tests pass.
- Existing deductible and SOAT retrieval behavior remains unchanged.
