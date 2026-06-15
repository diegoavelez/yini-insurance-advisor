# Plan

## Objective

Reduce `rag/ingestion.py` coupling by moving repeated batch-loop and failure-handling orchestration into a dedicated `rag` seam while preserving existing command outcomes and test patch points.

## Affected Files

- `rag/ingestion.py`
- `rag/ingestion_batch_runtime.py`
- `tests/test_ingestion.py`
- `tests/test_embedding_generation.py`
- `tests/test_qdrant_indexing.py`
- `specs/roadmap.md`
- `specs/2026-06-15-rag-batch-command-loop-and-failure-handling-seam-extraction/requirements.md`
- `specs/2026-06-15-rag-batch-command-loop-and-failure-handling-seam-extraction/plan.md`
- `specs/2026-06-15-rag-batch-command-loop-and-failure-handling-seam-extraction/validation.md`

## Assumptions

- Current batch-command tests already encode the intended `fail_fast`, fallback-record, and manifest-append behavior.
- Preserving wrappers or callable injection points in `rag.ingestion.py` is sufficient for existing tests.
- Top-level CLI dispatch should remain in `rag/ingestion.py` for this slice.

## Risks

- Generic loop extraction can accidentally hide command-specific error recovery differences.
- Changing callback signatures can break monkeypatch-heavy tests.

## Verification Strategy

- Run focused lint on touched files.
- Run ingestion, embedding-generation, and Qdrant-indexing tests that cover missing-directory exits, no-match exits, failure recovery, and `fail_fast` behavior.
- Keep command-specific recovery callbacks injectable where needed.
