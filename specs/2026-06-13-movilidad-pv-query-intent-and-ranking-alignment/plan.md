# Plan

## Objective

Improve movilidad PV benefit-intent retrieval by reusing the current curated
expansion and deterministic reranking path.

## Affected Files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-pv-query-intent-and-ranking-alignment/requirements.md`
- `specs/2026-06-13-movilidad-pv-query-intent-and-ranking-alignment/validation.md`

## Assumptions

- the core retrieval/reranking code already provides the needed execution seam;
- the main gap is missing curated PV benefit-intent anchors;
- the indexed PV chunks already contain the relevant benefit sections.

## Risks

- choosing anchors that are too broad and still match adjacent mobility guides;
- overfitting the rule to one phrasing while missing nearby operator wording;
- updating the roadmap without clearly stating that the scope is narrow.

## Steps

1. Add a curated PV benefit-intent query-expansion rule.
2. Add focused retrieval tests for augmentation and ranking.
3. Update the roadmap with the new corrective slice and note.
4. Run focused tests and lint.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched Python tests;
- rely on the already-captured live retrieval evidence as the pre-fix baseline,
  then request an operator rerun after merge if needed.
