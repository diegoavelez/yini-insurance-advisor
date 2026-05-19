# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 8 — LangGraph Workflow`.

The goal is to add a narrow planner step that selects among the existing tool
paths and linear workflow branches using typed routing decisions, without
introducing advanced recovery or multi-branch fallback behavior yet.

This slice should build directly on the completed linear workflow skeleton.

## In Scope

- Add one planner step to the LangGraph workflow.
- Add typed routing decisions over existing workflow/tool paths.
- Support explicit planner-level fallback behavior for unsupported routing
  choices.
- Preserve observability for planner decisions and workflow transitions.
- Add typed failure behavior for planner/runtime failures.

## Out of Scope

- Multi-branch recovery policies.
- Retry logic.
- Guardrails.
- MCP exposure.
- UI redesign.
- Advanced planner optimization.

## Execution Model

This slice should route only across already-implemented tool and workflow
surfaces.

At minimum:

1. Caller provides one user query.
2. Planner step classifies the query into one of the supported routing paths.
3. Workflow executes the selected path using existing typed tool seams.
4. Workflow returns typed final output or typed workflow failure.
5. Planner decisions remain observable.

The planner must not introduce hidden retrieval or side-channel behavior outside
existing tool boundaries.

## Planner Contract

The planner step must be typed and independently understandable.

At minimum:

- it should accept one user query;
- it should produce a typed routing decision;
- it should allow only explicitly supported routes;
- it should surface unsupported routing as a conservative valid workflow
  outcome or typed failure, per the selected contract.

## Routing Contract

This slice should keep routing narrow and explicit.

At minimum:

- routing should remain deterministic for the same input class;
- selected path should be traceable in workflow state and events;
- planner output should remain debuggable and constrained.

## Failure Contract

This slice should define a narrow, explicit error shape for planner callers.

At minimum, the workflow/planner error contract should distinguish:

- input validation failure;
- planner/runtime workflow failure;
- unsupported routing as a valid conservative workflow outcome.

Planner failures should remain observable while still returning structured
failure information to callers.

## Observability Contract

The workflow should preserve the current observability expectations.

At minimum:

- planner execution should remain correlated to a request id when one is
  provided;
- structured planner decision and transition events should be emitted;
- latency expectations should remain narrow and measurable.

## Acceptance Criteria

- A planner step exists in the workflow.
- Planner output is typed and constrained.
- At least one routed path executes over existing tools.
- Unsupported routing is handled conservatively.
- Planner decisions preserve observability behavior.
- The slice stops before advanced fallback or retry work.
