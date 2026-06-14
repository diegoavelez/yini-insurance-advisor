# Plan

## Objective

Enable and document a deterministic operator workflow for onboarding only the
remaining `choque simple` transversal PDFs as one cohort.

## Affected Files

- `Makefile`
- `docs/category-onboarding-playbook.md`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-choque-simple-corpus-completion-baseline/requirements.md`
- `specs/2026-06-13-movilidad-choque-simple-corpus-completion-baseline/validation.md`

## Assumptions

- The existing ingestion CLI already supports `--glob` for raw PDFs and glob
  filters for embeddings/indexing artifacts.
- The missing `choque simple` PDFs already have curated metadata overlays.

## Risks

- If the Makefile defaults are changed too broadly, operators could
  accidentally stop running full-tree batch jobs.

## Verification Strategy

- Use `make -n` to confirm the committed batch commands accept narrow glob
  overrides for ingestion, embeddings, and indexing.
- Re-read the playbook to verify the documented `choque simple` cohort
  commands are consistent with the Makefile surface.
