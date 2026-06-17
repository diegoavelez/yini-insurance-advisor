# Plan

## Objective

Align the current project docs with the product decision that `.docx` forms
are outside the MVP and should not be ingested or returned by the RAG system.

## Affected Files

- `README.md`
- `docs/category-onboarding-playbook.md`
- `specs/roadmap.md`
- `specs/2026-06-18-docx-mvp-exclusion-policy/requirements.md`
- `specs/2026-06-18-docx-mvp-exclusion-policy/validation.md`

## Assumptions

- the runtime is already PDF-only via `*.pdf` ingestion globs;
- the remaining work is current-source documentation and roadmap alignment.

## Risks

- leaving one current-source document with older "deferred" wording;
- overediting historical specs that should remain as evidence of previous
  planning.

## Steps

1. Add a dated spec bundle for the `.docx` MVP exclusion policy.
2. Update the roadmap to describe `.docx` PAC files as excluded from the MVP.
3. Update README and the onboarding playbook to state the PDF-only contract and
   the non-return posture for `.docx` forms.
4. Verify the current-source docs are consistent through focused grep review.

## Verification Strategy

- inspect the updated README, playbook, and roadmap wording directly;
- grep current-source docs for `.docx` references and confirm they now reflect
  exclusion rather than support.
