# Requirements

## Feature Summary

This feature defines the first narrow implementation slice of
`Phase 7 — Core Tooling`.

The goal is to expose the existing retrieval pipeline through a reusable,
independently callable tool layer with explicit tool-level success and failure
contracts.

This slice should reuse the current retrieval implementation and observability
work rather than creating a new retrieval path.

## In Scope

- Add a reusable `document_retrieval_tool` wrapper over the current retrieval
  seam.
- Define explicit tool-level success and failure behavior.
- Add typed error surface for tool callers.
- Preserve observability and latency expectations through the tool path.
- Keep the tool independently callable and locally testable.

## Out of Scope

- Clause extraction.
- Policy comparison.
- Citation verification.
- Response drafting.
- LangGraph orchestration.
- New retrieval algorithms or ranking changes.

## Execution Model

This slice should wrap the current retrieval implementation rather than replace
it.

At minimum:

1. Caller provides a typed retrieval query.
2. Tool invokes the existing retrieval pipeline.
3. Tool returns a typed success result or typed failure result.
4. Failures remain observable and explicit.

The tool may live in the current repository runtime without yet being wired into
an agent graph.

## Tool Contract

The retrieval tool must be independently callable and typed.

At minimum:

- it should accept the existing `RetrievalQuery` contract;
- it should return typed retrieved chunks on success;
- it should expose a typed error contract on failure;
- callers should not need to parse stderr or exception strings to understand
  expected tool failures.

## Failure Contract

This slice should define a narrow, explicit error shape for tool callers.

At minimum, the tool error contract should distinguish:

- configuration failure;
- dependency/runtime availability failure;
- backend execution failure;
- empty result as a valid non-error outcome.

Tool failures should remain fail-loud in logs while still returning typed,
structured failure information to the caller where appropriate.

## Observability Contract

The tool should preserve the current observability expectations.

At minimum:

- tool execution should remain correlated to a request id when one is provided;
- tool-level execution should remain observable through structured events;
- latency expectations should remain narrow and measurable.

## Acceptance Criteria

- `document_retrieval_tool` exists as an independently callable typed seam.
- Successful retrieval returns typed results through the tool contract.
- Empty retrieval remains a valid non-error tool outcome.
- Expected tool failures return structured error information.
- Tool execution preserves structured observability behavior.
- The slice stops before other tools or orchestration work.
