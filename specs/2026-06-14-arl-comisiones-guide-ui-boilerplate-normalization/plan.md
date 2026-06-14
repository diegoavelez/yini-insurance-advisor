# Plan

## Objective

Clean one ARL guide chunk by removing document-specific portal boilerplate
without changing broader ARL behavior.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-14-arl-comisiones-guide-ui-boilerplate-normalization/requirements.md`
- `specs/2026-06-14-arl-comisiones-guide-ui-boilerplate-normalization/plan.md`
- `specs/2026-06-14-arl-comisiones-guide-ui-boilerplate-normalization/validation.md`

## Assumptions

- the visible defect is limited to one current guide;
- document-specific markdown normalization is enough to recover a readable
  chunk surface;
- live indexing and retrieval infrastructure remain healthy.

## Risks

- removing a line that actually carries procedural meaning;
- leaving residual OCR noise that still affects answer citations;
- introducing a second ARL-specific normalization that overlaps the FAQ slice.

## Steps

1. Capture the current guide chunk boilerplate baseline.
2. Add narrow document-specific cleanup for the ARL commissions guide.
3. Add focused ingestion coverage for the cleaned guide surface.
4. Rebuild only the affected guide artifact from cached markdown.
5. Re-run live retrieval validation for the commissions guide query.

## Verification Strategy

- run focused ingestion tests and Ruff on touched files;
- inspect the rebuilt guide chunk bundle for the cleaned procedural surface;
- run live `retrieve-chunks` for an ARL commissions guide query.
