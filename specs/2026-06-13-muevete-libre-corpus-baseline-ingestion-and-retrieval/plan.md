# Plan

## Objective

Onboard `MOVILIDAD/MUEVETE LIBRE` with the smallest truthful baseline needed
for ingestion and retrieval.

## Affected Files

- `core/query_scope.py`
- `ops/term-equivalences.json`
- `ops/document-metadata-overlays.json`
- `tests/test_query_scope.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`

## Assumptions

- The current category scope is limited to the single clausulado PDF already in
  `data/raw`.
- `policy` is the correct retrieval-facing `document_type` for the baseline
  document.

## Risks

- Over-broad supported-scope tokens could admit unrelated `movilidad` queries.
- Canonical naming drift could fragment future retrieval filters.

## Verification Strategy

- run focused query-scope and ingestion tests;
- run lint on touched Python modules;
- run one real ingestion / embeddings / indexing / retrieval cycle for the new
  category if runtime dependencies are available.
