# Plan

## Objective

Reduce `rag/ingestion.py` coupling by moving deterministic manifest bookkeeping and artifact iteration behind a dedicated `rag` seam while preserving current batch command behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/ingestion_batch.py`
- `tests/test_ingestion.py`
- `tests/test_embedding_generation.py`
- `tests/test_qdrant_indexing.py`
- `specs/roadmap.md`
- `specs/2026-06-15-rag-manifest-recording-and-artifact-iteration-seam-extraction/requirements.md`
- `specs/2026-06-15-rag-manifest-recording-and-artifact-iteration-seam-extraction/plan.md`
- `specs/2026-06-15-rag-manifest-recording-and-artifact-iteration-seam-extraction/validation.md`

## Assumptions

- Existing ingestion, embedding, and indexing tests already encode the intended manifest and artifact-iteration behavior.
- Preserving thin wrappers in `rag.ingestion.py` is sufficient where tests patch or import those names directly.
- Batch command loops should remain the orchestration boundary for this slice.

## Risks

- Moving manifest helpers can break test patch points or drift timestamp/field population.
- Small iteration changes can alter deterministic ordering or glob matching in batch commands.

## Verification Strategy

- Run focused lint on touched files.
- Run ingestion, embedding, and indexing tests that cover manifest records and batch iteration.
- Preserve import/patch compatibility in `rag.ingestion.py` where current tests rely on it.
