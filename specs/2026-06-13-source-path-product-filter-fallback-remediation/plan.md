# Plan

## Objective

Allow product-filtered retrieval to keep relevant comparison chunks when product metadata is missing but the source-relative path clearly encodes the product.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-source-path-product-filter-fallback-remediation/requirements.md`
- `specs/2026-06-13-source-path-product-filter-fallback-remediation/validation.md`

## Assumptions

- source-relative paths remain stable and informative enough to infer product;
- the existing curated filter aliases provide the correct canonical product vocabulary;
- the fallback is most valuable in local hybrid recall before a fuller metadata backfill slice.

## Risks

- path inference could misclassify noisy folder names;
- fallback logic could drift from future ingestion metadata rules;
- semantic Qdrant hits with missing product still require future backfill if full parity is needed.

## Steps

1. Add canonical product inference from source-relative path.
2. Apply it only when chunk `product` is missing.
3. Use the fallback in local filter matching.
4. Add focused retrieval tests and update roadmap.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- re-run the AUTOS comparison retrieval query with `--product auto`.
