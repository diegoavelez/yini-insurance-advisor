# Plan

## Objective

Improve AUTOS comparative-query retrieval by adding a narrow operator-curated query-expansion rule seam.

## Affected Files

- `contracts/ingestion.py`
- `rag/ingestion.py`
- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `README.md`
- `specs/roadmap.md`

## Assumptions

- The retrieval miss is primarily caused by insufficient query-side lexical alignment rather than failed indexing.
- A deterministic curated rule seam is preferable to product-specific hardcoding in code.
- The comparative document remains the right evidence source for plan-difference questions.

## Risks

- Over-expanding AUTOS queries and diluting precise plan-specific searches.
- Encoding overly broad phrases that would fire on unrelated comparisons.
- Drifting curated canonical terms away from real document naming.

## Steps

1. Extend the term-equivalence contract with optional query-expansion rules.
2. Apply rule-based expansion after existing alias matching and deduplicate appended terms.
3. Add one AUTOS comparative-rule bundle in the curated operator file.
4. Add focused regression tests for positive and negative comparative cases.
5. Update README and roadmap with the new narrow slice.

## Verification Strategy

- Run focused pytest coverage for retrieval normalization.
- Run Ruff on touched Python files.
- Run one retrieval CLI query for the AUTOS comparison question and inspect whether the expanded query path succeeds without contract regressions.
