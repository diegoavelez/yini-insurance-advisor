# Requirements — hosted-smoke-expectations-and-operator-notes

## Objective

Document the narrow hosted smoke expectations and post-deploy operator notes
for the current hosted demo deployment path, without mixing in rollback,
runtime/dependency constraints, or demo-surface constraint notes.

## Scope

In scope:
- document the minimum hosted smoke expectations for the deployed demo;
- document narrow operator notes for checking the hosted surface after a
  deployment or rebuild;
- document the minimum post-deploy checks already supported by the current app
  and deployment posture.

Out of scope:
- rollback guidance;
- runtime/dependency constraints;
- supported-scope notes;
- guardrail/refusal notes;
- new hosted execution or automation work.

## Requirements

- Add a durable documentation surface for hosted smoke expectations and
  operator notes.
- Keep the notes aligned to the current hosted deployment posture:
  - Hugging Face Spaces;
  - root `README.md` Spaces config;
  - root `Dockerfile`;
  - current UI/app surface.
- Keep the notes concise and operator-oriented.
- Do not introduce undocumented hosted checks.

## Acceptance Criteria

- A durable documentation surface exists for hosted smoke expectations and
  operator notes.
- The documentation explicitly covers the minimum hosted checks expected after a
  deployment or rebuild of the current demo.
- The documentation does not drift into rollback guidance,
  runtime/dependency notes, or demo constraint notes.
