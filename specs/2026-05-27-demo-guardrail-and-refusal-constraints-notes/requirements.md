# Requirements — demo-guardrail-and-refusal-constraints-notes

## Objective

Document the narrow guardrail and refusal constraints that apply to the hosted
public demo, without mixing in supported-scope notes, runtime/dependency
constraints, or rollback procedure.

## Scope

In scope:
- document the current user-visible demo guardrail surfaces;
- document narrow refusal behaviors already evidenced by the current workflow
  and UI seams;
- document the current boundary between normal answer flow and conservative
  refusal/downgrade behavior.

Out of scope:
- supported-scope notes;
- runtime/dependency constraints;
- rollback playbooks;
- new UI behavior or new guardrail implementation.

## Requirements

- Add a durable documentation surface for demo guardrail and refusal
  constraints.
- Keep the notes aligned to the currently implemented behavior already visible
  in the app and tests.
- Keep the notes concise and user/operator-oriented.
- Do not introduce undocumented guardrails or refusal cases.

## Acceptance Criteria

- A durable documentation surface exists for demo guardrail/refusal
  constraints.
- The documentation explicitly covers the currently implemented prompt-
  injection refusal and conservative guardrail downgrade behavior only where
  already evidenced.
- The documentation explicitly distinguishes conservative refusal/downgrade
  behavior from normal answer flow.
- The documentation does not drift into runtime/dependency notes,
  supported-scope notes, or rollback procedure.
