# Plan

## Objective

Reduce `rag/ingestion.py` coupling by moving the grounded-answer helper cluster
 behind a dedicated `rag` seam while preserving current response behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/grounded_answers.py`
- `tests/test_grounded_answer_generation.py`
- `tests/test_observability.py`
- `specs/roadmap.md`
- `specs/2026-06-14-rag-grounded-answer-assembly-and-guardrails-seam-extraction/requirements.md`
- `specs/2026-06-14-rag-grounded-answer-assembly-and-guardrails-seam-extraction/plan.md`
- `specs/2026-06-14-rag-grounded-answer-assembly-and-guardrails-seam-extraction/validation.md`

## Assumptions

- The current grounded-answer helper behavior is already correct and should be
  preserved.
- Existing tests cover the key prompt, citation, refusal, and observability
  paths well enough to catch contract drift.
- Keeping `generate_grounded_answer()` in `rag/ingestion.py` preserves the
  intended orchestration boundary for now.

## Risks

- Partial extraction could leave helper behavior split awkwardly across
  modules.
- Changing refusal payload wording or citation derivation would break existing
  tests and downstream expectations.
- Over-expanding into retrieval or completion orchestration would blur the
  slice and increase validation cost.

## Verification Strategy

- Run focused grounded-answer and observability tests.
- Run focused lint on touched files.
- Re-run one live grounded-answer CLI query against the current collection.
