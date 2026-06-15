# Plan

## Objective

Reduce `rag/ingestion.py` coupling by moving the domain-specific evidence
selection and reranking cluster behind a dedicated `rag` seam while preserving
retrieval and answer behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/evidence_selection.py`
- `tests/test_retrieval.py`
- `tests/test_grounded_answer_generation.py`
- `tests/test_observability.py`
- `specs/roadmap.md`
- `specs/2026-06-14-rag-answer-evidence-selection-domain-seam-extraction/requirements.md`
- `specs/2026-06-14-rag-answer-evidence-selection-domain-seam-extraction/plan.md`
- `specs/2026-06-14-rag-answer-evidence-selection-domain-seam-extraction/validation.md`

## Assumptions

- The current domain heuristics are already behaviorally correct and should be
  preserved.
- Existing retrieval and grounded-answer tests cover the important evidence
  narrowing and reranking paths well enough to catch drift.
- Keeping top-level retrieval orchestration in `rag/ingestion.py` preserves the
  intended seam boundary for now.

## Risks

- The cluster is larger than the previous seam slices, so partial extraction
  could leave duplicate helpers or hidden constants behind.
- Changing even small intent heuristics could alter live retrieval results for
  specialized prompts.
- Over-expanding into lexical recall or query normalization would make the
  slice too broad.

## Verification Strategy

- Run focused retrieval, grounded-answer, and observability tests.
- Run focused lint on touched files.
- Re-run one live grounded-answer CLI query against the current collection.
