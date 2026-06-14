# Plan

## Objective

Remove duplicated heading scaffolds from ARL remuneration policy chunks without
changing policy coverage or ranking behavior.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-14-arl-remuneracion-policy-heading-dedup/requirements.md`
- `specs/2026-06-14-arl-remuneracion-policy-heading-dedup/plan.md`
- `specs/2026-06-14-arl-remuneracion-policy-heading-dedup/validation.md`

## Assumptions

- the duplication is produced during chunk assembly/prefix injection rather
  than missing corpus content;
- removing duplicated heading scaffolds is sufficient to improve readability
  without reclassifying the policy hierarchy.

## Risks

- stripping a heading that should remain visible because it adds unique
  hierarchy not represented in `section_path`;
- affecting other corpora that intentionally start with heading scaffolds.

## Steps

1. Capture the duplicated-heading baseline in current remuneration-policy
   chunks.
2. Add narrow chunk-assembly deduplication for leading heading scaffolds
   already covered by `section_path`.
3. Add focused ingestion coverage for duplicated-heading removal.
4. Rebuild the remuneration-policy artifact, regenerate its embeddings, and
   reindex it.
5. Re-run a live remuneration-policy retrieval query.

## Verification Strategy

- run focused ingestion tests and Ruff on touched files;
- inspect rebuilt remuneration-policy chunks for duplicate-heading removal;
- run live `retrieve-chunks` for one ARL remuneration query.
