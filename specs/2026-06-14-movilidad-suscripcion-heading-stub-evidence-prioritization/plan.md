# Plan

## Objective

Demote heading-only suscripción chunks so broad policy queries prefer richer
body evidence within the same policy family.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-suscripcion-section-structure-remediation/validation.md`
- `specs/2026-06-14-movilidad-suscripcion-heading-stub-evidence-prioritization/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-heading-stub-evidence-prioritization/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-heading-stub-evidence-prioritization/validation.md`

## Assumptions

- the current section structure is already good enough to support contentful
  chunk selection;
- the main remaining problem is that short heading-only chunks still receive
  too much score for broad suscripción policy prompts;
- a narrow deterministic reranking adjustment is sufficient before considering
  broader query-expansion work.

## Risks

- demoting short heading chunks too aggressively and hiding useful section
  anchors;
- applying the fix too broadly outside the suscripción policy family;
- improving one broad query while regressing specific section-navigation
  prompts.

## Steps

1. Capture the current heading-stub retrieval pattern for broad suscripción
   prompts.
2. Add the smallest deterministic preference for richer body chunks over
   heading-only stubs in this family.
3. Add focused regression coverage.
4. Re-run the suscripción live retrieval queries.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- re-run live suscripción policy retrieval queries.
