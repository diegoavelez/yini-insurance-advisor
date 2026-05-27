# Validation — deployment-rollback-notes

## Intended Validation

- Confirm a durable documentation surface exists for hosted deployment rollback
  notes.
- Confirm the notes match the current documented Spaces deployment path.
- Confirm the notes exclude hosted smoke expectations,
  runtime/dependency notes, and demo guardrail/scope notes.

## Executed Checks

- Verified the new `README.md` rollback section aligns with the current
  documented Spaces deployment posture:
  - root `README.md` YAML block with `sdk: docker`;
  - root `Dockerfile` as the authoritative build artifact;
  - rebuild/restart behavior on repo-state restoration.
- Verified the notes remain limited to rollback guidance and do not include
  hosted smoke expectations, runtime/dependency notes, or demo-surface
  constraints.

## Status

- Completed.
