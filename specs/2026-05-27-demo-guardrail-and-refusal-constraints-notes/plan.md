# Plan — demo-guardrail-and-refusal-constraints-notes

## Objective

Add narrow, durable notes covering only hosted demo guardrail and refusal
constraints.

## Affected Files

- `README.md`
- `specs/roadmap.md`
- `specs/2026-05-27-demo-guardrail-and-refusal-constraints-notes/requirements.md`
- `specs/2026-05-27-demo-guardrail-and-refusal-constraints-notes/plan.md`
- `specs/2026-05-27-demo-guardrail-and-refusal-constraints-notes/validation.md`

## Assumptions

- Existing app/UI seams and current tests are sufficient evidence for the
  documented guardrail/refusal posture.
- Supported-scope notes will be handled in the next slice, not here.

## Risks

- Notes could drift into supported-scope behavior if not kept narrow.
- Notes could overstate internal guardrail coverage beyond what is currently
  implemented and tested.

## Verification Strategy

- Verify the documentation aligns with the current UI surfaces and tested
  refusal/guardrail behaviors.
- Verify the notes remain limited to guardrail/refusal constraints.

## Status

- Completed.

## Completion Notes

- Added a dedicated guardrail/refusal constraints section to `README.md`.
- Kept the notes limited to currently evidenced prompt-injection refusal and
  conservative downgrade behavior for citation/confidence guardrails.
