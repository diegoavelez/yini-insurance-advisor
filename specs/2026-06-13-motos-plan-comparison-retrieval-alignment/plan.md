# Plan

## Objective

Improve `MOTOS` comparison-query evidence selection by activating the existing
comparison-intent retrieval path with one narrow operator-curated rule.

## Affected Files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-motos-plan-comparison-retrieval-alignment/requirements.md`
- `specs/2026-06-13-motos-plan-comparison-retrieval-alignment/validation.md`

## Assumptions

- the existing comparison candidate-pool expansion, local lexical recall, and
  reranking machinery is already generic enough to support `MOTOS`;
- the main missing ingredient is a category-specific comparison-intent rule;
- if the comparative artifact still loses after this change, the next slice
  should focus on representation/chunk quality rather than more retrieval
  policy.

## Risks

- the comparative table may still be too noisy even after rule-driven recall is
  activated;
- the query may improve partially but still not make `comparativo motos.pdf`
  the top result.

## Steps

1. Add one `motos` comparison query-expansion rule.
2. Add a focused retrieval test for that rule.
3. Record the slice in the roadmap.
4. Rerun the real `MOTOS` comparison retrieval and answer-query validations.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- rerun the real `MOTOS` comparison retrieval and answer query.
