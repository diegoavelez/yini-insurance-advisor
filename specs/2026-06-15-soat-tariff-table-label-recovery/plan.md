# Plan

## Objective

Preserve vehicle-category labels in the SOAT tariff document so tariff queries
return grounded labeled evidence instead of isolated numeric fragments.

## Affected files

- `rag/markdown_chunk_normalization.py`
- `tests/test_ingestion.py`
- `specs/2026-06-15-soat-tariff-table-label-recovery/validation.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`
- `specs/roadmap.md`

## Assumptions

- `MOVILIDAD/SOAT/tarifas soat 2026.pdf` is already onboarded and indexed;
- the primary failure is block/chunk structure, not query routing.

## Risks

- a too-broad table heuristic could rewrite unrelated tables incorrectly;
- the tariff PDF contains imperfect subgroup rows, so some model-year labels
  may remain approximate even after preserving the main vehicle family.

## Execution

1. Add the narrow corrective spec bundle.
2. Implement a SOAT tariff-table normalizer that rewrites one tariff table into
   vehicle-family statements.
3. Add focused ingestion tests for the normalized tariff text.
4. Rebuild the `tarifas soat 2026` artifacts and re-index them.
5. Validate live retrieval and grounded answering, then update matrix/roadmap.

## Verification strategy

- run focused `pytest` for markdown-block normalization;
- rerun ingestion/embeddings/indexing for `tarifas soat 2026.pdf`;
- rerun live `retrieve-chunks` and `answer-query` for
  `¿Cuáles son las tarifas SOAT 2026?`.
