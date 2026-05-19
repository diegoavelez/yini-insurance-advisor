# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 8 — LangGraph Workflow`.

The goal is to elevate the current routed workflow into a clearer
policy-analyst/verifier/drafter pass inside the graph, using the already
implemented reusable tools as explicit workflow stages.

This slice should strengthen workflow semantics and node boundaries without yet
introducing retry policies or advanced fallback recovery.

## In Scope

- Add an explicit analyst/verifier/drafter workflow pass.
- Keep composition over existing typed tools only.
- Make the comparison, verification, and drafting stages explicit in the graph.
- Preserve typed workflow output and typed workflow failure behavior.
- Preserve observability for workflow-stage transitions.

## Out of Scope

- Retry logic.
- Multi-branch recovery policies.
- Guardrails.
- MCP exposure.
- UI redesign.
- Planner optimization beyond the already-added routing step.

## Execution Model

This slice should refine workflow composition over already-implemented tool
surfaces.

At minimum:

1. Caller provides one user query.
2. Planner selects a supported route.
3. Workflow executes retrieval and extraction.
4. Workflow executes an explicit analyst pass over comparison.
5. Workflow executes an explicit verifier pass over evidence support.
6. Workflow executes an explicit drafting/finalization pass.
7. Workflow returns typed final output or typed workflow failure.

The workflow must not add hidden tool behavior outside existing tool
boundaries.

## Workflow Contract

The workflow pass must remain typed and explicitly staged.

At minimum:

- it should keep comparison, verification, and drafting as distinct workflow
  stages;
- it should pass typed state between those stages;
- it should return typed final workflow output or typed failure output.

## State Contract

This slice should refine, not replace, the shared workflow state.

At minimum:

- state should remain compatible with current contracts;
- analyst/verifier/drafter stage outputs should remain visible in state;
- state transitions should remain observable and debuggable.

## Failure Contract

This slice should preserve the current narrow error surface.

At minimum, the workflow error contract should distinguish:

- input validation failure;
- workflow/runtime failure;
- insufficient information as a valid non-error workflow outcome.

This slice should not introduce advanced retry or recovery behavior yet.

## Observability Contract

The workflow should preserve the current observability expectations.

At minimum:

- workflow execution should remain correlated to a request id when one is
  provided;
- structured analyst/verifier/drafter transition events should be emitted;
- latency expectations should remain narrow and measurable.

## Acceptance Criteria

- An explicit analyst/verifier/drafter pass exists in the workflow.
- Existing tools remain the underlying execution seams.
- Typed workflow output exists for success and failure.
- Workflow state exposes stage outputs clearly.
- Workflow transitions preserve observability behavior.
- The slice stops before retry/fallback policy work.
