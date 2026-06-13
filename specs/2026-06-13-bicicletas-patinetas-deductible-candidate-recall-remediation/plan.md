# Plan

Objective: make the local lexical recall layer surface explicit deductible
evidence ahead of adjacent but weaker chunks.

Affected files:
- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-bicicletas-patinetas-deductible-candidate-recall-remediation/requirements.md`
- `specs/2026-06-13-bicicletas-patinetas-deductible-candidate-recall-remediation/validation.md`

Assumptions:
- the remaining gap is localized to lexical candidate scoring;
- a deductible-intent section-label boost is sufficient for this pass.

Risks:
- overweighting deductible labels for unrelated products;
- coupling the scoring too tightly to one exact heading term.

Verification strategy:
- add focused retrieval tests for deductible candidate scoring;
- rerun retrieval tests and lint;
- rerun the real deductible query.
