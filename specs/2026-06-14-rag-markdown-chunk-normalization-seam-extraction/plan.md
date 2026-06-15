# Plan

## Objective

Reduce `rag/ingestion.py` coupling by extracting the stabilized markdown/chunk
normalization cluster into a dedicated module while preserving behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/markdown_chunk_normalization.py`
- `specs/roadmap.md`
- `specs/2026-06-14-rag-markdown-chunk-normalization-seam-extraction/requirements.md`
- `specs/2026-06-14-rag-markdown-chunk-normalization-seam-extraction/plan.md`
- `specs/2026-06-14-rag-markdown-chunk-normalization-seam-extraction/validation.md`

## Assumptions

- The current normalization and grouping behavior is correct and should be
  preserved.
- Reexport-by-import from `rag/ingestion.py` remains acceptable for test and
  caller compatibility.

## Risks

- The normalization cluster has many local helper dependencies, so an
  incomplete extraction could leave hidden coupling or import cycles.
- Accidentally moving chunk-boundary behavior instead of just normalization
  helpers would broaden the slice beyond the intended seam extraction.

## Verification Strategy

- Run focused ingestion tests that already cover normalized markdown and
  semantic block splitting.
- Run focused lint on touched files.
- Re-run one live `Muévete Libre` answer query and one live ARL remuneration
  answer query to confirm ingestion still imports and executes correctly.
