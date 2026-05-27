# Requirements — deployment-rollback-notes

## Objective

Document the narrow rollback guidance for the hosted demo deployment path,
without mixing in hosted smoke expectations, runtime/dependency notes, or
supported-scope/guardrail documentation.

## Scope

In scope:
- document the minimum rollback guidance for the current hosted deployment path;
- document how to revert to a previously known-good repo state for the hosted
  demo;
- document the minimum operator notes needed to undo a bad deployment change.

Out of scope:
- hosted smoke expectations;
- runtime/dependency constraints;
- supported-scope notes;
- guardrail/refusal notes;
- new automation or hosted execution work.

## Requirements

- Add a durable documentation surface for deployment rollback notes.
- Keep the notes aligned to the current hosted deployment posture:
  - Hugging Face Spaces;
  - root `README.md` Spaces config;
  - root `Dockerfile`.
- Keep the notes concise and operator-oriented.
- Do not introduce undocumented rollback mechanisms.

## Acceptance Criteria

- A durable documentation surface exists for deployment rollback notes.
- The documentation explicitly covers the minimum repo/operator steps needed to
  revert the hosted demo to a previously known-good state.
- The documentation does not drift into hosted smoke expectations,
  runtime/dependency notes, or demo guardrail/scope notes.
