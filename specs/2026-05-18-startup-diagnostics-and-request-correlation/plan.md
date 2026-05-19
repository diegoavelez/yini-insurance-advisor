# Plan

1. Observability Surface
   - Identify the current startup, UI request, and CLI execution seams.
   - Keep the slice scoped to existing runtime surfaces only.

2. Startup Diagnostics
   - Add one structured startup diagnostic event.
   - Include runtime mode and active non-secret configuration fields.

3. Request Correlation
   - Introduce a simple request identifier generator.
   - Propagate request ids through Gradio and current CLI execution paths.

4. Structured Execution Events
   - Add narrow structured events for request start, retrieval execution,
     grounded-answer execution, success, and failure.
   - Reuse the same event shape where practical.

5. Failure Logging
   - Emit structured correlated error events without weakening fail-loud
     behavior.

6. Validation Coverage
   - Add tests for startup diagnostics, request-id propagation, and structured
     failure logging.

7. Deferred Work Boundary
   - Stop before health endpoints, Phoenix activation, metrics backends, and
     broader observability expansion.
