# Plan

## Objective

Eliminate remaining metadata drift by persisting path-inferred canonical document types during ingestion when overlays are absent.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-source-path-document-type-metadata-backfill/requirements.md`
- `specs/2026-06-13-source-path-document-type-metadata-backfill/validation.md`

## Assumptions

- source-relative filenames and folders remain informative enough to infer document type;
- the term-equivalence file is the source of truth for canonical document-type vocabulary;
- overlay precedence must remain explicit and stable.

## Risks

- filename tokenization could misclassify ambiguous names;
- path-based document-type inference and future operator overlays could drift if not centralized.

## Steps

1. Reuse filter alias vocabulary to infer document type from path tokens.
2. Resolve overlay precedence explicitly.
3. Persist the resolved document type into processed and chunk artifacts.
4. Add focused ingestion tests and update roadmap.

## Verification Strategy

- run focused ingestion tests;
- run Ruff on touched files;
- spot-check regenerated comparison artifacts if needed.
