# Validation — demo-guardrail-and-refusal-constraints-notes

## Intended Validation

- Confirm a durable documentation surface exists for hosted demo
  guardrail/refusal constraints.
- Confirm the notes match currently implemented user-visible behavior.
- Confirm the notes exclude supported-scope notes, runtime/dependency notes,
  and rollback procedure.

## Executed Checks

- Verified the new `README.md` section aligns with currently implemented
  user-visible behavior evidenced by:
  - prompt-injection refusal behavior in `app/ui.py`;
  - citation-presence downgrade behavior in
    `tests/test_guardrail_abuse_cases.py`;
  - confidence-consistency downgrade behavior in
    `tests/test_guardrail_abuse_cases.py`.
- Verified the notes remain limited to guardrail/refusal constraints and do
  not include supported-scope notes, runtime/dependency notes, or rollback
  procedure.

## Status

- Completed.
