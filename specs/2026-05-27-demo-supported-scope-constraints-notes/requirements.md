# Requirements — demo-supported-scope-constraints-notes

## Objective

Document the narrow supported-scope constraints that apply to the hosted public
advisor demo, without mixing in guardrail/refusal notes, runtime/dependency
constraints, or rollback procedure.

## Scope

In scope:
- document the current supported-scope boundary for the hosted advisor demo;
- document narrow user-visible unsupported-scope behavior already evidenced by
  the current workflow and UI seams;
- document the current distinction between supported insurance-document
  questions and unsupported/out-of-scope requests.

Out of scope:
- guardrail/refusal notes unrelated to supported-scope behavior;
- runtime/dependency constraints;
- rollback playbooks;
- new UI behavior or new scope-classification logic.

## Requirements

- Add a durable documentation surface for demo supported-scope constraints.
- Keep the notes aligned to the currently implemented scope behavior already
  visible in the app and tests.
- Keep the notes concise and user/operator-oriented.
- Do not introduce undocumented supported-scope claims.

## Acceptance Criteria

- A durable documentation surface exists for demo supported-scope
  constraints.
- The documentation explicitly covers the currently implemented unsupported-
  scope refusal posture only where already evidenced.
- The documentation explicitly distinguishes supported insurance-document
  questions from unsupported/out-of-scope requests.
- The documentation does not drift into runtime/dependency notes,
  guardrail/refusal notes, or rollback procedure.
