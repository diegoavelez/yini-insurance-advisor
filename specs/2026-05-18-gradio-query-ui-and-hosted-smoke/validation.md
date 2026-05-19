# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- The app starts through the intended Gradio entrypoint.
- A successful query returns visible answer text, citations, confidence, and
  limitations.
- Insufficient-evidence responses are visible and distinguishable from runtime
  failures.
- Backend failures surface as explicit user-visible errors.
- A minimal hosted smoke request path executes without crashing.
- The implementation remains scoped to MVP UI exposure rather than advanced UX
  expansion.

## Merge Readiness

This spec is ready when the remaining `Phase 5` slice is decision-complete for:

- Gradio query UI wiring;
- typed grounded-response rendering;
- explicit UI failure handling;
- MVP startup and request smoke validation;

without drifting into advanced observability or orchestration work.
