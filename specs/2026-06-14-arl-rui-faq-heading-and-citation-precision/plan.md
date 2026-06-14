# Plan

## Objective

Make the `ARL/RUI` FAQ structurally semantic enough that live retrieval and
citations center on the exact numbered question evidence.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-14-arl-rui-faq-heading-and-citation-precision/requirements.md`
- `specs/2026-06-14-arl-rui-faq-heading-and-citation-precision/plan.md`
- `specs/2026-06-14-arl-rui-faq-heading-and-citation-precision/validation.md`

## Assumptions

- the problem is isolated to one current `ARL` FAQ document;
- structural cleanup at ingestion time is sufficient to improve live retrieval
  and citation precision;
- current Qdrant/Groq runtime remains healthy for live re-validation.

## Risks

- over-dropping adjacent FAQ content while removing the portal/status block;
- introducing duplicated question headings when some questions already arrive
  as markdown headings;
- needing a small retrieval-specific follow-up if semantic normalization alone
  does not fully narrow the answer evidence.

## Steps

1. Capture the current noisy-section and mixed-question baseline for the
   `ARL/RUI` FAQ.
2. Add narrow document-specific normalization that promotes numbered questions
   and strips the portal/status interruption.
3. Add focused ingestion coverage for the rewritten FAQ structure.
4. Rebuild only the affected FAQ artifact from cached markdown.
5. Re-run live retrieval and grounded-answer validation for the RUI
   normativity query.

## Verification Strategy

- run focused ingestion tests and Ruff on touched files;
- inspect the rebuilt FAQ chunk bundle for semantic question sections;
- re-run live `retrieve-chunks` and `answer-query` for the RUI normativity
  path.
