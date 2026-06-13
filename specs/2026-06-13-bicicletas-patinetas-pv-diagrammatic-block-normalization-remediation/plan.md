# Plan

Objective: improve semantic chunk inputs for the `pv` document in the current
`BICICLETAS Y PATINETAS` corpus without changing downstream contracts.

Affected files:
- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-bicicletas-patinetas-pv-diagrammatic-block-normalization-remediation/requirements.md`
- `specs/2026-06-13-bicicletas-patinetas-pv-diagrammatic-block-normalization-remediation/validation.md`

Assumptions:
- the main retrieval-quality issue is representational, not indexing-related;
- semantic section promotion and one narrow block normalizer are sufficient for
  this corrective pass.

Risks:
- over-normalizing ordinary paragraph blocks;
- promoting the wrong internal label as the governing section;
- silently dropping useful page-local content when skipping page headings.

Verification strategy:
- add focused tests for semantic section promotion, page-heading skipping, and
  coverage-block normalization;
- rerun targeted ingestion tests;
- reingest the `pv` artifact locally and inspect resulting chunks.
