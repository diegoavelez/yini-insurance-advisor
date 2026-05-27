# Requirements — demo-runtime-and-dependency-constraints-notes

## Objective

Document the narrow runtime and dependency constraints that govern the hosted
public demo deployment, without mixing in guardrail/scope notes or rollback
procedures.

## Scope

In scope:
- document the current hosted runtime assumptions for the demo;
- document the minimum required runtime environment variables;
- document narrow dependency/runtime caveats already evidenced by the current
  Docker, startup, readiness, and Spaces slices.

Out of scope:
- demo guardrail or supported-scope limitations;
- rollback playbooks;
- new deployment automation or hosted execution work.

## Requirements

- Add a narrow documentation surface for demo runtime and dependency
  constraints.
- Keep the notes aligned to the current authoritative deployment path:
  - root `Dockerfile`;
  - root `README.md` Spaces config;
  - current startup-variable contract.
- Keep the notes concise and operator-oriented.
- Do not introduce undocumented runtime requirements.

## Acceptance Criteria

- A durable documentation surface exists for demo runtime and dependency
  constraints.
- The documentation explicitly covers the minimum runtime variables currently
  required by the app startup contract.
- The documentation explicitly covers the current hosted runtime posture
  already selected for Hugging Face Spaces.
- The documentation does not drift into guardrail/scope notes or rollback
  procedure.
