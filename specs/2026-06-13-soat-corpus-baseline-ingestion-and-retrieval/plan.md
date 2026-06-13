# Plan

## Objective

Onboard `MOVILIDAD/SOAT` into the current RAG baseline with the smallest
taxonomy, scope, and metadata alignment needed before any runtime retrieval
corrections.

## Affected Files

- `core/query_scope.py`
- `ops/term-equivalences.json`
- `ops/document-metadata-overlays.json`
- `tests/test_ingestion.py`
- `tests/test_query_scope.py`
- `specs/roadmap.md`
- `specs/2026-06-13-soat-corpus-baseline-ingestion-and-retrieval/requirements.md`
- `specs/2026-06-13-soat-corpus-baseline-ingestion-and-retrieval/validation.md`

## Assumptions

- `product=soat` is the narrowest truthful canonical taxonomy for this corpus;
- `tarifas soat 2026.pdf` can start as `document_type=guide` without expanding
  the current document-type contract;
- real runtime validation should happen only after the baseline is committed.

## Risks

- `tarifas soat 2026.pdf` may later need date-aware or tariff-specific
  retrieval handling;
- some user vocabulary may mention only the expanded insurance name and require
  additional aliases later.

## Steps

1. Add `soat` query/filter aliases and scope tokens.
2. Add curated overlays for the two SOAT documents.
3. Add focused query-scope and ingestion regressions.
4. Record the slice in the roadmap.
5. Run targeted validation.

## Verification Strategy

- run focused query-scope and ingestion tests;
- run Ruff on touched files;
- confirm the roadmap includes the new completed slice.
