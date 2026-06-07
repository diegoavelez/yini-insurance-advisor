# Requirements — hosted-spaces-deployment-validation-and-evidence

## Objective

Perform and document one real Hugging Face Spaces deployment validation for the
current demo, recording durable evidence that the hosted deployment exists and
that the minimum post-deploy smoke checks were actually run.

## Scope

In scope:
- validate one real hosted deployment of the current demo to Hugging Face
  Spaces;
- record the deployed Space URL;
- record the deployed commit SHA;
- record the actual post-deploy smoke results for the minimum hosted checks.

Out of scope:
- rollback guidance;
- broader productionization work;
- speculative documentation without deployment evidence;
- changes to demo behavior unrelated to deployment validation.

## Requirements

- Add a durable evidence surface for one real hosted deployment validation.
- Keep the evidence aligned to the current hosted deployment posture:
  - Hugging Face Spaces;
  - root `README.md` Spaces config;
  - root `Dockerfile`.
- Record only actually observed hosted facts.
- Do not claim a successful public deployment without a concrete URL and
  matching deployed commit SHA.

## Acceptance Criteria

- A durable documentation surface exists for hosted deployment evidence.
- The documentation explicitly records:
  - Space URL;
  - deployed commit SHA;
  - actual hosted smoke results.
- `Phase 14` completion claims are updated only after this evidence exists.
