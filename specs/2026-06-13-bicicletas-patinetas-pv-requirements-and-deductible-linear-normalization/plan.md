# Plan

Objective: make the remaining `pv` line-grid sections more semantically useful
before embeddings and retrieval.

Affected files:
- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-bicicletas-patinetas-pv-requirements-and-deductible-linear-normalization/requirements.md`
- `specs/2026-06-13-bicicletas-patinetas-pv-requirements-and-deductible-linear-normalization/validation.md`

Assumptions:
- the remaining quality gap is local to two line-grid sections;
- deterministic rule-based rewriting is sufficient for the current corpus.

Risks:
- mis-grouping values across adjacent rows;
- over-normalizing non-grid paragraphs in the same sections.

Verification strategy:
- add focused unit tests for both section normalizers;
- rerun targeted ingestion tests and lint;
- reingest the `pv` file and inspect the resulting chunks.
