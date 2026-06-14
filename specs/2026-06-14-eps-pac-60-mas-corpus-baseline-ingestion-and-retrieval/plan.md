# Plan

## Objective

Prepare the repository for truthful onboarding of the `PAC 60+ core` cohort as
the first `EPS/PLAN COMPLEMENTARIO PAC` baseline, while documenting the
remaining cohorts and deferrals.

## Affected files

- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json`
- `core/query_scope.py`
- `tests/test_ingestion.py`
- `tests/test_retrieval.py`
- `tests/test_query_scope.py`
- `specs/roadmap.md`

## Assumptions

- the canonical product for this folder should be `pac`;
- `PAC 60+` and `plan complementario PAC` should normalize into that same
  product family;
- `.docx` files remain out of scope until ingestion explicitly supports them;
- the first operational onboarding should stop at the five `PAC 60+ core` PDFs
  rather than the full folder.

## Risks

- `PAC 60+` and future `PAC tradicional` queries will share the same canonical
  product and may later need document-family disambiguation;
- shorter operational PAC guides may require additional supported-scope tokens
  or family rules once their cohorts are onboarded;
- the two large PDFs may still need extraction-specific remediation after their
  isolated runs.

## Execution

1. Add `PAC 60+` aliases, supported-scope tokens, and baseline overlays.
2. Add focused regression coverage for PAC product inference, overlay
   persistence, retrieval alias normalization, and supported-scope admission.
3. Create this spec bundle for the `PAC 60+ core` baseline cohort.
4. Update the roadmap so the next onboarding target and the deferred PAC
   cohorts are explicit.

## Verification strategy

- run focused `pytest` checks for ingestion, retrieval, and query scope;
- verify the baseline cohort is documented as five PDFs only;
- verify the deferred `.docx` posture and the large-PDF isolation rule are
  visible in the spec bundle and roadmap.

