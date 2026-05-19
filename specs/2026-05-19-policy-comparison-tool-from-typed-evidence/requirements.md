# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 7 — Core Tooling`.

The goal is to expose policy comparison as an independently callable tool over
typed evidence and extracted clauses, with structured comparison output and
explicit insufficient-information behavior.

This slice should build on the existing retrieval and clause-extraction tool
layers rather than introducing new retrieval or orchestration behavior.

## In Scope

- Add a reusable `policy_comparison_tool`.
- Accept typed evidence and/or extracted clauses as input.
- Produce structured comparison points.
- Add explicit insufficient-information behavior.
- Add typed tool-level failure behavior.
- Preserve observability and request correlation where provided.

## Out of Scope

- Running retrieval inside the comparison tool.
- Performing clause extraction inside the comparison tool.
- Citation verification.
- Response drafting.
- LangGraph orchestration.
- UI behavior changes.

## Execution Model

This slice should operate only on already-typed upstream evidence.

At minimum:

1. Caller provides typed evidence and/or extracted clauses.
2. Tool compares the available inputs conservatively.
3. Tool returns typed comparison output or typed failure output.
4. Insufficient information remains a valid non-error outcome.

The tool should not perform a new retrieval call or hidden extraction step.

## Tool Contract

The policy comparison tool must be independently callable and typed.

At minimum:

- it should accept typed evidence inputs;
- it should return structured comparison points on success;
- it should expose a typed failure contract on failure;
- it should make insufficient-information outcomes explicit without treating them
  as runtime failures.

## Comparison Contract

This slice should produce conservative comparison output.

At minimum:

- comparison points must be traceable to source documents or supporting clauses;
- the tool should avoid inventing differences when evidence is weak;
- the tool should surface notes when evidence is insufficient for strong
  comparison claims.

## Failure Contract

This slice should define a narrow, explicit error shape for policy comparison
tool callers.

At minimum, the tool error contract should distinguish:

- input validation failure;
- comparison/runtime failure;
- insufficient information as a valid non-error outcome.

Tool failures should remain observable while still returning structured failure
information to callers.

## Observability Contract

The tool should preserve the current observability expectations.

At minimum:

- tool execution should remain correlated to a request id when one is provided;
- structured tool execution events should be emitted;
- latency expectations should remain narrow and measurable.

## Acceptance Criteria

- `policy_comparison_tool` exists as an independently callable typed seam.
- Successful comparison returns structured comparison points.
- Insufficient information remains a valid non-error result.
- Expected tool failures return structured error information.
- Tool execution preserves observability behavior.
- The slice stops before citation verification, drafting, or orchestration work.
