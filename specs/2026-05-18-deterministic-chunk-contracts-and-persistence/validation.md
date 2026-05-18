# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- The implementation defines a typed chunk contract for cleaned Markdown
  outputs.
- The existing ingestion CLI exposes explicit chunk configuration flags.
- Chunk size and overlap behavior are explicit and testable.
- The same cleaned Markdown input produces the same chunk boundaries across
  reruns.
- The same cleaned Markdown input and configuration produce the same
  `chunk_id` values across reruns.
- Persisted chunk artifacts are written to deterministic local paths at
  `data/processed/chunks/<source_pdf_id>.chunks.json`.
- Chunk metadata includes propagated traceability fields from processed
  documents.
- Partial chunk-generation failures are not treated as successful completion.
- The implementation remains local-only and does not introduce embeddings or
  Qdrant integration.

## Merge Readiness

This spec is ready when the first `Phase 3` slice is decision-complete for:

- deterministic chunk contracts;
- stable chunk identifiers;
- explicit chunk settings;
- local chunk persistence;
- traceable metadata propagation;

without drifting into indexing, retrieval ranking, or answer generation.
