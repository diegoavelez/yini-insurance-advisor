# Requirements

## Feature Summary

This feature defines the second narrow slice of
`Phase 17 — Runtime Compatibility Hardening`.

The goal is to remove the remaining mismatch between the validated Groq runtime
identifier and the repository defaults/operators docs so deployments do not
silently fall back to an unsupported model id.

## In Scope

- Align the typed `Settings` default for `groq_model` with the validated
  runtime identifier.
- Extend the hosted runtime contract notes so `GROQ_MODEL` is treated as part
  of the minimum operator-facing startup surface.
- Add focused regression coverage for the aligned default/runtime contract.

## Out of Scope

- Re-validating end-to-end retrieval or generation behavior.
- Changing providers or model families.
- Modifying Qdrant or embedding configuration behavior.
- Hosted Space secret management changes.

## Acceptance Criteria

- `Settings.groq_model` defaults to `openai/gpt-oss-120b`.
- Operator-facing runtime contract notes include `GROQ_MODEL` wherever the
  minimum hosted startup surface is listed.
- Focused config/smoke tests fail if the default Groq model drifts from the
  documented runtime contract.
