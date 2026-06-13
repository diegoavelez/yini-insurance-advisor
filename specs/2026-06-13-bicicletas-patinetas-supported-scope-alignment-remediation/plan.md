# Plan

Objective: remove the deterministic supported-scope rejection for benign
Spanish bicycle and scooter insurance questions in the current corpus.

Affected files:
- `core/query_scope.py`
- `tests/test_query_scope.py`
- `specs/roadmap.md`
- `specs/2026-06-13-bicicletas-patinetas-supported-scope-alignment-remediation/requirements.md`
- `specs/2026-06-13-bicicletas-patinetas-supported-scope-alignment-remediation/validation.md`

Assumptions:
- the remaining end-to-end gap is limited to deterministic scope admission;
- narrow product vocabulary is sufficient for this remediation.

Risks:
- over-broadening supported scope with generic transport vocabulary;
- masking unrelated scope failures if the token additions are too broad.

Verification strategy:
- add a focused query-scope regression test for the representative Spanish
  bicycle/scooter query;
- rerun focused tests for `query_scope` plus the ingestion regression file;
- rerun a real end-to-end `answer-query` validation after the code change.
