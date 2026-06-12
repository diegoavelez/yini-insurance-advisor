# Plan

## Objective

Add a minimal, repeatable operator workflow for running Docling ingestion and
embeddings from an external local virtualenv.

## Affected Files

- `Makefile`
- `README.md`
- `specs/roadmap.md`
- `specs/2026-06-12-external-batch-runtime-operator-flow/requirements.md`
- `specs/2026-06-12-external-batch-runtime-operator-flow/validation.md`

## Assumptions

- the external batch runtime remains a local operator concern;
- a configurable `Makefile` surface is sufficient for the current scope;
- machine-specific runtime paths should live in overrides, not committed code.

## Risks

- overfitting to one workstation path;
- accidentally implying the app runtime should also move off `.venv`;
- adding helper commands that drift from the canonical ingestion CLI contract.

## Verification Strategy

- verify the new batch targets expand to the expected ingestion commands;
- run at least one real target against the validated external runtime and
  temporary output directories;
- confirm the documented operator flow matches the validated commands.
