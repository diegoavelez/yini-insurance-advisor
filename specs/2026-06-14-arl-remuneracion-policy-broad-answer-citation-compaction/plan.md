# Plan

## Objective

Reduce citation and documentary-basis noise for broad ARL remuneration-policy
answers while preserving the existing answer and retrieval quality.

## Affected Files

- `rag/ingestion.py`
- `tests/test_grounded_answer_generation.py`
- `specs/roadmap.md`
- `specs/2026-06-14-arl-remuneracion-policy-broad-answer-citation-compaction/requirements.md`
- `specs/2026-06-14-arl-remuneracion-policy-broad-answer-citation-compaction/plan.md`
- `specs/2026-06-14-arl-remuneracion-policy-broad-answer-citation-compaction/validation.md`

## Assumptions

- The current broad ARL remuneration answer is already supported and does not
  need retrieval or prompt changes.
- Citation compaction can be implemented as a narrow selection rule over
  already-retrieved evidence.

## Risks

- Over-compaction could remove a chunk that the generated answer still relies
  on, causing weaker grounding.
- If the section names drift in future source revisions, the compact-support
  anchors may need refresh.

## Verification Strategy

- Add focused grounded-answer coverage for broad ARL remuneration overview
  prompts.
- Run focused `pytest` against grounded-answer and retrieval ARL paths.
- Run one live `answer-query` validation for the broad ARL remuneration query.
