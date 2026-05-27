# Validation — demo-supported-scope-constraints-notes

## Intended Validation

- Confirm a durable documentation surface exists for hosted demo
  supported-scope constraints.
- Confirm the notes match currently implemented user-visible behavior.
- Confirm the notes exclude guardrail/refusal notes, runtime/dependency notes,
  and rollback procedure.

## Executed Checks

- Verified the new `README.md` section aligns with currently implemented
  user-visible behavior evidenced by:
  - unsupported-scope refusal behavior in `app/ui.py`;
  - unsupported-scope demo output assertions in
    `tests/test_guardrail_abuse_cases.py`.
- Verified the notes remain limited to supported-scope constraints and do not
  include guardrail/refusal notes, runtime/dependency notes, or rollback
  procedure.

## Status

- Completed.
