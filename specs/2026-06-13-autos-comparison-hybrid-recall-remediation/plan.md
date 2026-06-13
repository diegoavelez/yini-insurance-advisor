# Plan

## Objective

Add a narrow deterministic hybrid recall path so comparison documents can surface even when semantic retrieval alone misses them.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-autos-comparison-hybrid-recall-remediation/requirements.md`
- `specs/2026-06-13-autos-comparison-hybrid-recall-remediation/validation.md`

## Assumptions

- persisted local chunk artifacts are available in normal runtime environments;
- comparison-intent rules are an adequate activation gate for the first hybrid slice;
- a simple lexical overlap scorer is sufficient before adding heavier retrieval infrastructure.

## Risks

- lexical scoring could over-surface noisy chunks if too broad;
- local corpus scanning could add latency if not tightly scoped;
- duplicate candidate fusion could distort scores if not deterministic.

## Steps

1. Add local chunk-corpus loader and filter-aware lexical scorer.
2. Activate lexical recall only for matched comparison rules.
3. Merge lexical and semantic candidates deterministically.
4. Reuse existing reranking over the merged pool.
5. Add focused retrieval tests and update roadmap.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- validate the real AUTOS comparison query after reindex if needed.
