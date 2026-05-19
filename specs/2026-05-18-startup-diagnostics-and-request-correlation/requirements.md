# Requirements

## Feature Summary

This feature defines the first narrow implementation slice of
`Phase 6 — Baseline Observability`.

The goal is to make the current MVP diagnosable without expanding into full
tracing, metrics platforms, or advanced observability tooling.

This slice should introduce explicit startup diagnostics, request correlation,
and structured execution/error events across the current CLI and Gradio
entrypoints.

## In Scope

- Add startup diagnostics for the active runtime mode and key configuration.
- Introduce per-request correlation identifiers.
- Propagate request identifiers through the current grounded QA execution seam.
- Emit structured log events around retrieval and grounded-answer execution.
- Define a minimal shared error-event shape for current CLI and UI entrypoints.
- Keep the implementation narrow, explicit, and locally testable.

## Out of Scope

- Full tracing backends.
- Distributed tracing.
- Advanced latency dashboards.
- Phoenix activation beyond what later Phase 6 slices define.
- Hosted health/readiness endpoints.
- Tool-level observability for future tools not yet implemented.

## Execution Model

This slice should cover the current runtime surfaces only:

1. Startup path for the Gradio app entrypoint.
2. Request execution path for the Gradio query handler.
3. Existing CLI paths that run ingestion, embedding, indexing, retrieval, and
   grounded answering.

The implementation should not add a new runtime surface.

## Startup Diagnostics Contract

At startup, the system should emit a structured diagnostic event that makes the
current runtime mode inspectable.

At minimum, the event should make visible:

- `deployment_mode`
- `app_env`
- active `groq_model`
- active `embedding_provider`
- active `embedding_model`
- active `qdrant_collection`
- `top_k`

Secrets must never be logged.

## Request Correlation Contract

Each top-level request or command execution should receive a request identifier.

At minimum:

- the Gradio query path should generate a request id per submitted query;
- the current grounded QA path should log retrieval and answer-generation events
  with that request id;
- CLI entrypoints should emit execution events with a request id for the active
  command invocation.

The identifier format only needs to be stable and human-inspectable for this
slice; cryptographic properties are not required.

## Structured Event Contract

This slice should define a minimal event shape for logging current runtime
activity.

At minimum, events should distinguish:

- startup diagnostics;
- request start;
- request success;
- request failure;
- retrieval execution;
- grounded-answer execution.

The event shape should be narrow and shared where practical, without introducing
heavy abstractions.

## Failure Behavior

If retrieval, grounded answering, or a top-level CLI command fails:

- the error should remain fail-loud;
- a structured error event should be emitted with request correlation;
- the slice must not swallow or downgrade real failures.

## Acceptance Criteria

- Startup diagnostics are emitted without leaking secrets.
- The Gradio query path uses request correlation ids.
- The current grounded QA execution path emits structured retrieval and
  answer-generation events.
- CLI entrypoints emit correlated execution events.
- Failures surface through explicit structured error events.
- The slice stops before full tracing, metrics backends, or hosted health checks.
