# Plan

## Objective

Ensure explicit ARL account-update answers cite only the guide that already
contains the full update procedure.

## Affected Files

- `rag/ingestion.py`
- `tests/test_grounded_answer_generation.py`
- `specs/roadmap.md`
- `specs/2026-06-14-arl-cuenta-bancaria-guide-family-answer-evidence-alignment/requirements.md`
- `specs/2026-06-14-arl-cuenta-bancaria-guide-family-answer-evidence-alignment/plan.md`
- `specs/2026-06-14-arl-cuenta-bancaria-guide-family-answer-evidence-alignment/validation.md`

## Assumptions

- the account-update guide remains a sufficient primary retrieval result;
- the remaining gap is limited to answer-facing evidence narrowing.

## Risks

- over-filtering account-update-adjacent guide evidence for nearby ARL guide
  queries;
- accidentally lowering confidence if the narrowed citation set interacts badly
  with grounding guardrails.

## Steps

1. Capture the current account-update answer-evidence baseline.
2. Add a narrow citation/doc-basis selector for explicit account-update guide
   intent.
3. Add focused grounded-answer coverage.
4. Re-run live `answer-query` validation for the account-update guide query.

## Verification Strategy

- run focused grounded-answer tests and Ruff on touched files;
- verify live `answer-query` returns only the account-update guide in
  documentary basis and citations.
