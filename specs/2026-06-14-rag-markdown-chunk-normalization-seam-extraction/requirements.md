# Requirements

## Slice

`rag-markdown-chunk-normalization-seam-extraction`

## Goal

Extract document-specific markdown normalization plus semantic block
normalization/chunk-grouping helpers out of `rag/ingestion.py` into a dedicated
`rag` seam without changing current chunking behavior.

## Context

After the ARL-remuneration and document-canonicalization extractions,
`rag/ingestion.py` still owns a large cohesive normalization cluster covering:

- known-document markdown rewrites for `suscripción`, `Muévete Libre`, ARL/RUI,
  ARL commissions, and `choque simple` guides;
- block-level normalization for comparison tables, diagrammatic coverage,
  expedition requirements, deductible grids, `choque simple` circulars, and PV
  commercial text;
- semantic block splitting and grouping helpers used before chunk assembly.

That cluster is now the last explicitly documented post-onboarding refactor
candidate.

## Requirements

1. Markdown normalization and semantic block/grouping helpers must move to a
   dedicated module under `rag/`.
2. `rag/ingestion.py` must import and use that seam rather than keep the
   normalization cluster inline.
3. Current behavior must remain unchanged for the validated paths, especially:
   - known-document normalization for `suscripción`, `Muévete Libre`, ARL/RUI,
     ARL commissions, and `choque simple`;
   - PV/comparison/deductible/circular block normalization;
   - semantic `section_path` preservation used by current chunking logic.
4. Existing focused tests and current live retrieval/answer validations for the
   normalized corpora must continue to pass.

## Non-Goals

- changing chunk boundary policy;
- changing retrieval ranking heuristics;
- changing contracts or artifact schemas.
