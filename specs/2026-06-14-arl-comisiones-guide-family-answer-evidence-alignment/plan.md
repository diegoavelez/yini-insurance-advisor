# Plan

## Objective

Ensure explicit ARL commissions guide answers cite only the guide that already
contains the full procedure.

## Affected Files

- `rag/ingestion.py`
- `tests/test_grounded_answer_generation.py`
- `specs/roadmap.md`
- `specs/2026-06-14-arl-comisiones-guide-family-answer-evidence-alignment/requirements.md`
- `specs/2026-06-14-arl-comisiones-guide-family-answer-evidence-alignment/plan.md`
- `specs/2026-06-14-arl-comisiones-guide-family-answer-evidence-alignment/validation.md`

## Assumptions

- the commissions guide remains the first and sufficient retrieval result;
- the remaining gap is answer-evidence selection, not retrieval ranking.

## Risks

- over-filtering ARL guide evidence for adjacent operational queries;
- unintentionally lowering confidence if the narrowed set becomes too small for
  grounding guardrails.

## Steps

1. Capture the current commissions answer-evidence baseline.
2. Add a narrow answer-evidence selector for explicit ARL commissions guide
   intent.
3. Add focused grounded-answer coverage for the narrowed citation path.
4. Re-run live `answer-query` validation for the commissions guide query.

## Verification Strategy

- run focused grounded-answer tests and Ruff on touched files;
- verify live `answer-query` returns only the commissions guide in citations
  and documentary basis.
