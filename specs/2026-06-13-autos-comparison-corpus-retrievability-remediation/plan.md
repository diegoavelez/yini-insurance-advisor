# Plan

## Objective

Make fragmented comparison PDFs more retrievable by greedily aggregating short consecutive blocks within the same section.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-autos-comparison-corpus-retrievability-remediation/requirements.md`
- `specs/2026-06-13-autos-comparison-corpus-retrievability-remediation/validation.md`

## Assumptions

- the comparative document is present in the corpus but loses semantic competitiveness because key labels are split across tiny blocks;
- greedy same-section aggregation is safer than introducing document-specific templates;
- chunk size remains the natural upper bound.

## Risks

- merging blocks that are adjacent but semantically weakly related;
- changing chunk composition for some existing documents;
- increasing chunk text length enough to alter retrieval elsewhere.

## Steps

1. Replace pairwise same-section grouping with greedy same-section accumulation.
2. Preserve current heading and clause-marker special cases.
3. Add regression tests for multi-block same-section aggregation.
4. Regenerate and reindex the AUTOS comparative document.
5. Measure retrieval again.

## Verification Strategy

- run focused chunking tests;
- run Ruff on touched files;
- regenerate the comparative chunk bundle, embeddings, and Qdrant points;
- rerun the AUTOS comparison retrieval query.
