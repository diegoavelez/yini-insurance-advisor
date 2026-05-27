# Validation — demo-runtime-and-dependency-constraints-notes

## Intended Validation

- Confirm a durable documentation surface exists for hosted demo runtime and
  dependency constraints.
- Confirm the notes match the current Docker/Spaces/runtime-variable posture.
- Confirm the notes exclude guardrail/scope notes and rollback procedure.

## Executed Checks

- Verified the new `README.md` section aligns with:
  - the root Spaces config block (`sdk: docker`, `app_port: 7860`);
  - the authoritative root `Dockerfile`;
  - the current startup-variable contract (`GROQ_API_KEY`, `QDRANT_URL`,
    `QDRANT_API_KEY`).
- Verified the notes remain limited to runtime/dependency constraints and do
  not include guardrail/scope notes or rollback procedure.

## Status

- Completed.
