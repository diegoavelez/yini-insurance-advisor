# Plan

## Objective

Turn embedding-runtime readiness into an explicit operator seam with immediate,
actionable failure behavior when model assets are unavailable offline.

## Affected Files

- `rag/ingestion.py`
- `tests/test_embedding_generation.py`
- `specs/roadmap.md`
- `specs/2026-06-13-embedding-runtime-readiness-validation/requirements.md`
- `specs/2026-06-13-embedding-runtime-readiness-validation/validation.md`

## Assumptions

- The sentence-transformers package is installed, but the configured model may
  be absent from the local Hugging Face cache.

## Risks

- If the offline-first behavior is too strict, operators may mistake cache
  absence for a package-installation issue unless the error message is precise.

## Verification Strategy

- Add targeted tests for warm-up and offline failure.
- Run the embedding-generation CLI against the current `PV` chunk glob and
  verify immediate actionable failure.
- Attempt a live warm-up only if the environment permits networked execution.
