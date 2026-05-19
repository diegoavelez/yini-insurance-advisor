# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 7 — Core Tooling`.

The goal is to expose citation verification as an independently callable tool
that checks whether drafted output remains supported by the cited evidence, with
structured verification output and explicit failure behavior.

This slice should build on the existing retrieval, clause-extraction,
comparison, and grounded-answer layers without introducing orchestration.

## In Scope

- Add a reusable `citation_verifier_tool`.
- Accept drafted output plus cited evidence as typed input.
- Produce structured verification output.
- Add explicit valid non-error behavior for unsupported or weakly supported
  claims.
- Add typed tool-level failure behavior.
- Preserve observability and request correlation where provided.

## Out of Scope

- Running retrieval inside the verifier.
- Performing clause extraction inside the verifier.
- Policy comparison.
- Response drafting.
- LangGraph orchestration.
- UI behavior changes.

## Execution Model

This slice should operate only on already-typed upstream inputs.

At minimum:

1. Caller provides drafted output text and typed cited evidence.
2. Tool evaluates support conservatively against the provided evidence only.
3. Tool returns typed verification output or typed failure output.
4. Unsupported or weakly supported claims remain valid non-error outcomes.

The tool must not perform hidden retrieval or drafting.

## Tool Contract

The citation verifier tool must be independently callable and typed.

At minimum:

- it should accept drafted output plus typed citations/evidence inputs;
- it should return structured verification output on success;
- it should expose a typed failure contract on failure;
- it should make unsupported or weakly supported outcomes explicit without
  treating them as runtime failures.

## Verification Contract

This slice should produce conservative verification output.

At minimum:

- verification output must remain traceable to cited evidence;
- the tool should avoid overstating support when evidence is weak;
- the tool should surface notes when support is partial or insufficient.

## Failure Contract

This slice should define a narrow, explicit error shape for citation verifier
callers.

At minimum, the tool error contract should distinguish:

- input validation failure;
- verification/runtime failure;
- unsupported or weakly supported results as valid non-error outcomes.

Tool failures should remain observable while still returning structured failure
information to callers.

## Observability Contract

The tool should preserve the current observability expectations.

At minimum:

- tool execution should remain correlated to a request id when one is provided;
- structured tool execution events should be emitted;
- latency expectations should remain narrow and measurable.

## Acceptance Criteria

- `citation_verifier_tool` exists as an independently callable typed seam.
- Successful verification returns structured verification output.
- Weak or unsupported support remains a valid non-error result.
- Expected tool failures return structured error information.
- Tool execution preserves observability behavior.
- The slice stops before drafting or orchestration work.
