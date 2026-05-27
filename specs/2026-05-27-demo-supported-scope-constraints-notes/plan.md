# Plan — demo-supported-scope-constraints-notes

## Objective

Add narrow, durable notes covering only hosted demo supported-scope
constraints.

## Affected Files

- `README.md`
- `specs/roadmap.md`
- `specs/2026-05-27-demo-supported-scope-constraints-notes/requirements.md`
- `specs/2026-05-27-demo-supported-scope-constraints-notes/plan.md`
- `specs/2026-05-27-demo-supported-scope-constraints-notes/validation.md`

## Assumptions

- Existing app/UI seams and current tests are sufficient evidence for the
  documented supported-scope posture.
- Rollback and hosted-smoke notes remain separate and will be handled later.

## Risks

- Notes could drift into guardrail/refusal behavior if not kept narrow.
- Notes could overstate supported coverage beyond what is currently implemented
  and tested.

## Verification Strategy

- Verify the documentation aligns with the current UI surfaces and tested
  unsupported-scope behavior.
- Verify the notes remain limited to supported-scope constraints.

## Status

- Completed.

## Completion Notes

- Added a dedicated supported-scope constraints section to `README.md`.
- Kept the notes limited to the currently evidenced unsupported-scope refusal
  posture and the distinction between supported insurance-document questions
  and unsupported requests.
