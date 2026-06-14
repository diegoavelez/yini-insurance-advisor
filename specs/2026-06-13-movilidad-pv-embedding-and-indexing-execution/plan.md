# Plan

## Objective

Run the `PV` cohort through embeddings, Qdrant indexing, and a live retrieval
check now that corpus and runtime blockers have been reduced.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-pv-embedding-and-indexing-execution/requirements.md`
- `specs/2026-06-13-movilidad-pv-embedding-and-indexing-execution/validation.md`

## Assumptions

- The operator has already run `python -m rag.ingestion warmup-embedding-assets`
  successfully in a machine/session with network access.
- Current environment variables for Qdrant remain valid.

## Risks

- Network restrictions in the harness may block Qdrant indexing even when the
  code and credentials are correct.
- Live retrieval could still expose a narrow corpus issue not visible in local
  chunk audits.

## Verification Strategy

- Generate embeddings only for `movilidad__transversales__pv-*.chunks.json`.
- Index only `movilidad__transversales__pv-*.embeddings.json`.
- Run a retrieval/query check scoped to `product=movilidad` and
  `document_type=guide`.
