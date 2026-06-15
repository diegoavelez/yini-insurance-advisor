# Plan

## Objective

Reduce `rag/ingestion.py` coupling by moving the cohesive runtime/provider bridge cluster into a dedicated `rag` seam while preserving existing warmup, retrieval, and answer behaviors.

## Affected Files

- `rag/ingestion.py`
- `rag/runtime_providers.py`
- `tests/test_ingestion.py`
- `tests/test_embedding_generation.py`
- `tests/test_retrieval.py`
- `tests/test_grounded_answer_generation.py`
- `tests/test_observability.py`
- `specs/roadmap.md`
- `specs/2026-06-15-rag-runtime-provider-and-warmup-seam-extraction/requirements.md`
- `specs/2026-06-15-rag-runtime-provider-and-warmup-seam-extraction/plan.md`
- `specs/2026-06-15-rag-runtime-provider-and-warmup-seam-extraction/validation.md`

## Assumptions

- Existing tests already encode the intended runtime/provider behavior and patch points.
- `rag.ingestion.py` must continue exposing wrappers or aliases for names that tests import or monkeypatch directly.
- Warmup commands should remain lightweight wrappers around the extracted runtime seam.

## Risks

- Moving cached loader helpers can break cache clearing or monkeypatch surfaces.
- Small changes to import paths or exception messages can break focused runtime tests.

## Verification Strategy

- Run focused lint on touched files.
- Run embedding-generation, retrieval, grounded-answer, observability, and ingestion tests that cover runtime/provider behavior.
- Preserve compatibility wrappers in `rag.ingestion.py` wherever the tests currently import or patch runtime helpers.
