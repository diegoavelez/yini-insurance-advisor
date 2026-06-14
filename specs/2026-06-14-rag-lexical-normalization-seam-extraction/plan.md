# Plan

## Objective

Create a narrow lexical-normalization seam in `rag` before additional category
onboarding increases coupling inside `rag/ingestion.py`.

## Affected Files

- `rag/ingestion.py`
- `rag/term_equivalences.py`
- `tests/test_term_equivalences.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-rag-lexical-normalization-seam-extraction/requirements.md`
- `specs/2026-06-14-rag-lexical-normalization-seam-extraction/plan.md`
- `specs/2026-06-14-rag-lexical-normalization-seam-extraction/validation.md`

## Assumptions

- the extracted helper functions are pure or near-pure and can move without
  changing retrieval behavior;
- keeping the function names imported into `rag.ingestion` is sufficient to
  preserve current test imports and call sites.

## Risks

- introducing an import cycle between the new helper module and
  `rag/ingestion.py`;
- accidentally changing normalization behavior while relocating helper logic;
- under-scoping the slice by moving orchestration code that still belongs in
  `rag/ingestion.py`.

## Steps

1. Create a dedicated lexical helper module for term-equivalence normalization.
2. Rewire `rag/ingestion.py` to import the extracted helpers.
3. Add focused helper-level tests for normalization, phrase matching, and
   term loading.
4. Update roadmap traceability for this preventive corrective slice.

## Verification Strategy

- run focused lexical and retrieval tests;
- run Ruff on touched Python files;
- confirm `rag/ingestion.py` no longer defines the extracted lexical helpers.
