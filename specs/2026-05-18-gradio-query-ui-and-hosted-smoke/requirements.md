# Requirements

## Feature Summary

This feature defines the remaining narrow implementation slice of
`Phase 5 — Basic RAG MVP`.

The goal is to expose the existing grounded retrieval-and-answer backend
through the first real Gradio query interface and add minimal hosted smoke
behavior for the public MVP path.

This slice should make the system usable as a demo without yet expanding into
advanced observability, tooling, or orchestration concerns.

## In Scope

- Build the first Gradio query interface on top of the grounded QA pipeline.
- Wire the existing grounded-answer backend into a user-triggered UI flow.
- Show answer text, citations, confidence, and limitations in the UI.
- Provide explicit user-visible failure behavior for retrieval and generation
  errors.
- Add minimal hosted startup and request smoke checks for the MVP path.
- Keep the deployment-facing interaction surface narrow and testable.

## Out of Scope

- Complex multi-pane UX.
- Conversation history or multi-turn state.
- Streaming responses.
- Advanced visual polish.
- Multi-agent controls.
- Full observability instrumentation beyond what is strictly needed for smoke
  readiness.

## Execution Model

This slice should expose a simple app entrypoint suitable for local execution
and hosted MVP deployment.

The execution path should be:

1. User enters a query.
2. UI invokes the grounded QA backend.
3. UI renders the typed response fields.
4. Errors are shown explicitly in a user-visible form.
5. Hosted smoke checks confirm the app starts and can serve a basic request
   path.

## UI Contract

This slice should use Gradio as defined in the tech stack.

At minimum, the UI should expose:

- a query input;
- a submit action;
- answer text output;
- citations display;
- confidence display;
- limitations or insufficiency display.

The UI must not invent or reshape backend data in ways that break traceability.

## Backend Integration Contract

This slice must reuse the existing typed grounded-answer pipeline rather than
implementing duplicate answer logic in the UI layer.

At minimum:

- the UI should call a single typed backend seam;
- retrieval and answer-generation failures must propagate into explicit UI
  error states;
- successful responses must preserve citations and advisor-review messaging.

## Failure Behavior

If the grounded QA backend fails:

- the UI must show an explicit error state;
- users must not receive a fake successful answer;
- insufficient-evidence responses must remain distinguishable from runtime
  failures.

## Hosted Smoke Contract

This slice should add the minimum checks needed to trust the MVP hosting path.

At minimum:

- the app must start successfully with the expected startup path;
- a minimal request path must execute without crashing;
- smoke checks must remain narrow and operational, not full UX testing.

## Acceptance Criteria

- A user can enter a query through Gradio and receive the grounded typed
  response.
- Citations, confidence, and limitations are visible in the UI.
- Retrieval/generation failures surface as explicit UI errors.
- Hosted startup and request smoke checks exist for the MVP path.
- The slice stops before advanced UX, observability expansion, or orchestration.
