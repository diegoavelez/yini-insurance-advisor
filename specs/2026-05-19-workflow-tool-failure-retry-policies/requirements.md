# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 8 — LangGraph Workflow`.

The goal is to add bounded retry behavior for selected tool and runtime
failures inside the existing workflow, while preserving typed terminal-failure
outcomes and observable retry transitions.

This slice should stay focused on narrow retry policy only and should not add a
broader recovery tree or new planner behavior.

## In Scope

- Add explicit retry boundaries for selected workflow tool/runtime failures.
- Preserve typed workflow failure output after retry exhaustion.
- Preserve observability for retry attempts and terminal failures.
- Keep retry behavior deterministic and narrowly scoped.

## Out of Scope

- Insufficient-evidence fallback behavior.
- Multi-branch recovery trees.
- Planner redesign.
- Guardrails.
- MCP exposure.
- UI redesign.

## Execution Model

This slice should refine the existing routed workflow over current tool seams.

At minimum:

1. Workflow executes the current routed path.
2. If a selected tool/runtime failure occurs at an allowed retry boundary,
   workflow retries a bounded number of times.
3. If retries succeed, workflow continues normally.
4. If retries are exhausted, workflow returns a typed terminal-failure result.
5. Retry transitions and terminal failures remain observable.

Retry behavior must be explicit and limited to the stages defined by this spec.

## Retry Contract

The retry behavior must be explicit and deterministic.

At minimum:

- retries should apply only to selected workflow stages;
- retry count should be bounded and stable;
- non-retryable failures should fail immediately;
- exhausted retries should produce a typed workflow failure rather than an
  untyped crash.

## Failure Contract

This slice should preserve the narrow workflow error surface.

At minimum, the workflow error contract should still distinguish:

- input validation failure;
- retryable workflow/runtime failure;
- terminal workflow/runtime failure after retry exhaustion;
- insufficient information as a valid non-error workflow outcome.

This slice should not change planner routing behavior.

## Observability Contract

The workflow should preserve the current observability expectations.

At minimum:

- retry attempts should remain correlated to a request id when one is provided;
- structured retry events should be emitted for each attempt;
- terminal failure after exhaustion should emit a distinct structured event;
- latency visibility should remain narrow and measurable.

## Acceptance Criteria

- Explicit retry boundaries exist for selected workflow stages.
- Retryable failures are retried a bounded number of times.
- Non-retryable failures fail immediately with typed workflow failure output.
- Retry exhaustion returns a typed terminal-failure result.
- Retry attempts and terminal failures are traceable in state and events.
- The slice stops before broader recovery-tree work.
