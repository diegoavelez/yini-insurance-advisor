# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 7 — Core Tooling`.

The goal is to expose clause extraction as an independently callable tool over
retrieved evidence only, with typed clause categorization and explicit tool
failure behavior.

This slice should build on the existing retrieval contracts and the typed
`Clause` contract already present in the repository.

## In Scope

- Add a reusable `clause_extraction_tool`.
- Accept retrieved evidence rather than raw user queries.
- Produce typed `Clause` outputs with explicit categories.
- Add typed tool-level failure behavior.
- Preserve observability and request correlation where provided.

## Out of Scope

- Running retrieval inside the clause extraction tool.
- Policy comparison.
- Citation verification.
- Response drafting.
- LangGraph orchestration.
- Advanced legal or semantic normalization beyond this narrow clause-extraction
  slice.

## Execution Model

This slice should operate only on retrieved evidence.

At minimum:

1. Caller provides retrieved chunks.
2. Tool extracts zero or more typed clauses from those chunks.
3. Tool returns typed success or typed failure output.
4. Empty clause extraction remains a valid non-error outcome.

The tool should not perform a new retrieval call itself.

## Tool Contract

The clause extraction tool must be independently callable and typed.

At minimum:

- it should accept retrieved evidence as input;
- it should return typed `Clause` outputs on success;
- it should expose a typed failure contract on failure;
- it should preserve supporting chunk traceability.

## Clause Categorization Contract

This slice should classify extracted clauses into the existing clause categories
already defined in the repository.

At minimum:

- extracted clauses must use the existing `ClauseCategory` values;
- supporting chunk ids must remain traceable;
- clause extraction should stay conservative rather than inventing categories or
  unsupported summaries.

## Failure Contract

This slice should define a narrow, explicit error shape for clause extraction
tool callers.

At minimum, the tool error contract should distinguish:

- input validation failure;
- extraction/runtime failure;
- empty extraction as a valid non-error outcome.

Tool failures should remain observable while still returning structured failure
information to callers.

## Observability Contract

The tool should preserve the current observability expectations.

At minimum:

- tool execution should remain correlated to a request id when one is provided;
- structured tool execution events should be emitted;
- latency expectations should remain narrow and measurable.

## Acceptance Criteria

- `clause_extraction_tool` exists as an independently callable typed seam.
- Successful extraction returns typed `Clause` outputs.
- Empty extraction remains a valid non-error result.
- Supporting chunk ids remain traceable in outputs.
- Expected tool failures return structured error information.
- The slice stops before retrieval orchestration, comparison, or drafting work.
