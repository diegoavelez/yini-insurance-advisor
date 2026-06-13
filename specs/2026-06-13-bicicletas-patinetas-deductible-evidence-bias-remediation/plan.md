# Plan

Objective: make deductible-intent queries prefer explicit deductible sections
when those sections are already present in retrieval candidates.

Affected files:
- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-bicicletas-patinetas-deductible-evidence-bias-remediation/requirements.md`
- `specs/2026-06-13-bicicletas-patinetas-deductible-evidence-bias-remediation/validation.md`

Assumptions:
- the remaining gap is ranking bias, not ingestion or indexing;
- a section-level lexical preference is sufficient for this correction.

Risks:
- over-biasing unrelated deductible mentions in other products;
- disrupting existing ranking for non-deductible queries.

Verification strategy:
- add focused retrieval tests for deductible-intent reranking;
- rerun targeted retrieval tests and lint;
- rerun the real end-to-end deductible query.
