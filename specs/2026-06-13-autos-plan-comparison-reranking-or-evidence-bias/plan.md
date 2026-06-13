# Plan

## Objective

Improve AUTOS comparison-query evidence selection with deterministic rule-driven reranking over a larger candidate pool.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `README.md`
- `specs/roadmap.md`
- `specs/2026-06-13-autos-plan-comparison-reranking-or-evidence-bias/requirements.md`
- `specs/2026-06-13-autos-plan-comparison-reranking-or-evidence-bias/validation.md`

## Assumptions

- the comparative document exists in Qdrant but is being crowded out by stronger FAQ lexical overlap;
- a larger candidate pool plus deterministic lexical bias is enough to surface better evidence;
- rule-driven matching is preferable to hardcoded document-specific logic.

## Risks

- boosting weak but keyword-heavy chunks too aggressively;
- increasing candidate-pool size more than necessary;
- unintentionally reordering non-comparison queries.

## Steps

1. Reuse matched query-expansion rules as the comparison-intent signal.
2. Increase Qdrant candidate limit only for those queries.
3. Rerank candidates deterministically using curated appended-term matches.
4. Add focused tests for reranking and unchanged non-comparison behavior.
5. Update roadmap/docs with the new slice.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched Python files;
- run one real AUTOS comparison retrieval query to inspect the new top results.
