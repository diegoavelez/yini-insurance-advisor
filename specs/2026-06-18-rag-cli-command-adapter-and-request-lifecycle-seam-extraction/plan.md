# Plan

## Objective

Reduce backend coupling in the CLI entrypoint by extracting shared command
adapters and request lifecycle orchestration from `rag/ingestion.py` without
changing CLI behavior.

## Affected Files

- `rag/cli_runtime.py`
- `rag/ingestion.py`
- `tests/test_cli_runtime.py`
- `specs/roadmap.md`
- `specs/2026-06-18-rag-cli-command-adapter-and-request-lifecycle-seam-extraction/requirements.md`
- `specs/2026-06-18-rag-cli-command-adapter-and-request-lifecycle-seam-extraction/validation.md`

## Assumptions

- the current CLI parser and command flags are already correct and should
  remain unchanged;
- this slice is a structural extraction, not a behavioral remediation;
- existing observability event names remain the source of truth.

## Risks

- changing request lifecycle control flow could break existing observability
  tests or request correlation;
- duplicating too much logic inside the new seam would only move coupling
  instead of reducing it;
- moving too much beyond adapters and lifecycle would exceed the documented
  slice.

## Steps

1. Add a dedicated CLI runtime seam for adapters, shared query construction,
   and request lifecycle orchestration.
2. Refactor `rag/ingestion.py` into a façade over that seam while preserving
   parser definitions and lower-level runtime helpers.
3. Add focused regression tests for query building and lifecycle behavior.
4. Sync the roadmap to mark the slice closed and document the residual
   `rag/ingestion.py` scope.
5. Run targeted validation.

## Verification Strategy

- run focused CLI runtime, observability, retrieval, and grounded-answer tests;
- run Ruff on touched files;
- manually confirm that `rag/ingestion.py` still owns parser definitions while
  the new seam owns adapters and lifecycle orchestration.
