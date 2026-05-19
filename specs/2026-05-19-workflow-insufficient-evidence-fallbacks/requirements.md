# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 8 — LangGraph Workflow`.

The goal is to add explicit insufficient-evidence fallback behavior to the
workflow, so weak or incomplete evidence leads to a conservative typed workflow
outcome with observable fallback transitions.

This slice should remain focused on non-error fallback behavior only and should
not introduce retry logic for tool/runtime failures.

## In Scope

- Add explicit insufficient-evidence fallback edges in the workflow.
- Preserve typed workflow output for conservative fallback outcomes.
- Preserve observability for fallback decisions and transitions.
- Keep fallback behavior deterministic and narrow.

## Out of Scope

- Retry logic.
- Tool/runtime retry policies.
- Multi-branch recovery trees.
- Guardrails.
- MCP exposure.
- UI redesign.

## Execution Model

This slice should refine the existing workflow over current tool seams.

At minimum:

1. Workflow executes the current routed path.
2. If evidence is weak or insufficient at defined stages, workflow follows an
   explicit fallback edge.
3. Workflow returns a conservative typed response instead of a runtime error.
4. Fallback transitions remain observable.

The workflow must not introduce retry behavior in this slice.

## Fallback Contract

The fallback behavior must be explicit and typed.

At minimum:

- insufficient evidence should remain a valid non-error workflow outcome;
- fallback output should preserve conservative confidence and review messaging;
- fallback path should remain traceable in workflow state and events.

## Failure Contract

This slice should preserve the current narrow error surface.

At minimum, the workflow error contract should still distinguish:

- input validation failure;
- workflow/runtime failure;
- insufficient information as a valid non-error workflow outcome.

This slice should not change tool/runtime retry behavior.

## Observability Contract

The workflow should preserve the current observability expectations.

At minimum:

- fallback execution should remain correlated to a request id when one is
  provided;
- structured fallback transition events should be emitted;
- latency expectations should remain narrow and measurable.

## Acceptance Criteria

- Explicit insufficient-evidence fallback edges exist in the workflow.
- Weak or insufficient evidence returns a conservative typed workflow result.
- Fallback transitions are traceable in state and events.
- Workflow remains scoped to non-error fallback behavior only.
- The slice stops before retry-policy work.
