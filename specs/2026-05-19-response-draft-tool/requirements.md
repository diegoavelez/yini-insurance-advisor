# Requirements

## Feature Summary

This feature defines the final narrow implementation slice of
`Phase 7 — Core Tooling`.

The goal is to expose response drafting as an independently callable tool that
builds advisor-facing draft responses from already-typed upstream evidence,
while preserving explicit confidence, limitations, citations, and review
notice behavior.

This slice should build on the existing retrieval, comparison, verification,
and grounded-answer layers without introducing orchestration.

## In Scope

- Add a reusable `response_draft_tool`.
- Accept typed upstream evidence and verification inputs.
- Produce typed `AdvisorDraftResponse` output.
- Add explicit insufficient-information behavior.
- Add typed tool-level failure behavior.
- Preserve observability and request correlation where provided.

## Out of Scope

- Running retrieval inside the drafting tool.
- Performing clause extraction inside the drafting tool.
- Policy comparison inside the drafting tool.
- Citation verification inside the drafting tool.
- LangGraph orchestration.
- UI behavior changes.

## Execution Model

This slice should operate only on already-typed upstream inputs.

At minimum:

1. Caller provides a user query plus typed evidence, citations, and optional
   verification/comparison context.
2. Tool drafts a conservative advisor-facing response from those typed inputs
   only.
3. Tool returns typed draft output or typed failure output.
4. Insufficient information remains a valid non-error outcome.

The tool must not perform hidden retrieval, verification, or orchestration.

## Tool Contract

The response draft tool must be independently callable and typed.

At minimum:

- it should accept typed drafting inputs;
- it should return structured draft output on success;
- it should expose a typed failure contract on failure;
- it should make insufficient-information outcomes explicit without treating
  them as runtime failures.

## Drafting Contract

This slice should produce conservative advisor-facing output.

At minimum:

- drafted output must remain traceable to supplied citations and documentary
  basis;
- the tool should avoid overstating certainty when evidence is weak;
- the tool should surface limitations and the advisor review notice
  consistently.

## Failure Contract

This slice should define a narrow, explicit error shape for drafting callers.

At minimum, the tool error contract should distinguish:

- input validation failure;
- drafting/runtime failure;
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

- `response_draft_tool` exists as an independently callable typed seam.
- Successful drafting returns typed `AdvisorDraftResponse` output.
- Insufficient information remains a valid non-error result.
- Expected tool failures return structured error information.
- Tool execution preserves observability behavior.
- The slice stops before orchestration work.
