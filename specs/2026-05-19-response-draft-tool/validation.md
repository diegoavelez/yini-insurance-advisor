# Validation

## Status

- Implementation complete on `2026-05-19`.
- Verification completed with:
  - `ruff check .`
  - `pytest`

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- Successful drafting returns typed `AdvisorDraftResponse` output.
- Insufficient information remains a valid non-error result.
- Draft output remains traceable to supplied citations and documentary basis.
- Validation/runtime failures return typed error information.
- Tool execution remains observable and correlated when request ids are present.
- The implementation remains scoped to drafting only.

## Merge Readiness

This spec is ready when the final `Phase 7` slice is decision-complete for:

- independently callable response drafting behavior;
- structured draft outputs and failure contracts;
- preserved observability expectations;

without drifting into LangGraph orchestration.
