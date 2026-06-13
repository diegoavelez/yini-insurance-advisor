# Plan

## Objective

Eliminate product-metadata drift by persisting path-inferred canonical products during ingestion when overlays are absent.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-source-path-product-metadata-backfill/requirements.md`
- `specs/2026-06-13-source-path-product-metadata-backfill/validation.md`

## Assumptions

- source-relative path segments remain stable enough to encode canonical product families;
- the term-equivalence file is the source of truth for canonical product vocabulary;
- historical artifact backfill can happen later if needed.

## Risks

- path inference could misclassify noisy folder structures;
- ingestion-time inference and retrieval-time fallback could diverge if not reused from one helper.

## Steps

1. Reuse the source-path product inference helper during ingestion.
2. Resolve overlay precedence explicitly.
3. Persist the resolved product into processed and chunk artifacts.
4. Add focused ingestion tests and update roadmap.

## Verification Strategy

- run focused ingestion tests;
- run Ruff on touched files;
- spot-check the regenerated AUTOS comparative artifacts if needed.
