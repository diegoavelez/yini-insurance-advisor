# Requirements

## Feature Summary

This feature defines the first narrow implementation slice of
`Phase 8 — LangGraph Workflow`.

The goal is to introduce LangGraph wiring, a shared workflow state, and one
linear end-to-end workflow path over the already-implemented reusable tools,
without adding planner branching or advanced fallback behavior yet.

This slice should prove that the current tool surfaces can be composed through a
single observable workflow skeleton.

## In Scope

- Add LangGraph project wiring.
- Add one shared workflow state for the workflow path.
- Add one linear graph path over existing typed tool seams.
- Preserve observability for workflow-state transitions.
- Add explicit typed failure behavior for workflow execution.

## Out of Scope

- Planner branching.
- Advanced routing logic.
- Retry/fallback policy beyond one conservative failure path.
- MCP exposure.
- UI redesign.
- Guardrail behavior.

## Execution Model

This slice should compose already-typed reusable tools only.

At minimum:

1. Caller provides one user query.
2. Workflow builds shared state.
3. Workflow executes a linear path using existing tool layers.
4. Workflow returns a typed end-to-end result or typed workflow failure.
5. State transitions remain observable.

The workflow must not add hidden retrieval logic outside the existing tool
boundaries.

## Workflow Contract

The workflow skeleton must be independently callable and typed.

At minimum:

- it should accept one user query;
- it should maintain shared state across graph nodes;
- it should compose existing tools in one linear order;
- it should return typed final output or typed workflow failure.

## State Contract

This slice should define the first workflow state boundary.

At minimum:

- state should remain compatible with current shared contracts;
- state should expose enough fields for retrieval, verification, and drafting;
- state transitions should remain observable and debuggable.

## Failure Contract

This slice should define a narrow, explicit error shape for workflow callers.

At minimum, the workflow error contract should distinguish:

- input validation failure;
- tool/runtime workflow failure;
- insufficient information as a valid non-error workflow outcome.

Workflow failures should remain observable while still returning structured
failure information to callers.

## Observability Contract

The workflow should preserve the current observability expectations.

At minimum:

- workflow execution should remain correlated to a request id when one is
  provided;
- structured workflow transition events should be emitted;
- latency expectations should remain narrow and measurable.

## Acceptance Criteria

- LangGraph is wired into the project.
- One shared workflow state exists.
- One linear workflow path composes the existing tools.
- Typed workflow output exists for success and failure.
- State transitions preserve observability behavior.
- The slice stops before planner branching or advanced fallback work.
