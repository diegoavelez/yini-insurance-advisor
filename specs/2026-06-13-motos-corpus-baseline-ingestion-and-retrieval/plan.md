# Plan

## Objective

Onboard `MOVILIDAD/MOTOS` into the current RAG baseline with the smallest
metadata and document-type alignment needed before any category-specific
retrieval remediation.

## Affected Files

- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-motos-corpus-baseline-ingestion-and-retrieval/requirements.md`
- `specs/2026-06-13-motos-corpus-baseline-ingestion-and-retrieval/validation.md`

## Assumptions

- the existing `moto` product taxonomy is sufficient for this phase;
- overlay metadata is the narrowest truthful way to stabilize retrieval-facing
  classification for the first four documents;
- comparison-specific ranking issues, if any, should be handled only after a
  real retrieval miss is observed.

## Risks

- `comparativo motos.pdf` may later expose the same structural retrieval issues
  that AUTOS comparison documents exposed;
- future operator vocabulary may still require a follow-on alias or reranking
  slice after live retrieval validation.

## Steps

1. Add curated overlays for the four `MOTOS` documents.
2. Extend guide document-type inference to cover `comparativo`.
3. Add a focused ingestion regression for `comparativo motos.pdf`.
4. Record the slice in the roadmap.
5. Run targeted ingestion validation.

## Verification Strategy

- run focused ingestion tests;
- run Ruff on touched ingestion-related files;
- confirm the roadmap includes the new completed slice.
