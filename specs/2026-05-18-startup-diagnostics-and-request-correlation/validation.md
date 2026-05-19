# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- Startup emits a structured diagnostic event with non-secret configuration.
- The Gradio request path assigns and propagates a request id.
- Retrieval and grounded-answer execution emit correlated structured events.
- CLI command execution emits correlated structured events.
- Runtime failures emit explicit structured error events.
- No secrets appear in startup or execution logs.

## Merge Readiness

This spec is ready when the first `Phase 6` slice is decision-complete for:

- startup diagnostics;
- request correlation;
- structured retrieval/answer execution logging;
- explicit correlated failure events;

without drifting into health endpoints, Phoenix activation, or broader tracing
work.
