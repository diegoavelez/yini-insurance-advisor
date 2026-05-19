# Plan

1. UI Entry Contract
   - Replace the placeholder app entrypoint with a real Gradio-backed query UI.
   - Keep the app layer thin and delegate to the grounded QA backend.

2. Backend Wiring
   - Connect the UI submit flow to the existing grounded-answer generation seam.
   - Preserve typed response handling rather than duplicating business logic.

3. Response Rendering
   - Display answer text, citations, confidence, and limitations clearly.
   - Keep the rendered structure traceable to backend response fields.

4. Failure States
   - Show explicit user-visible errors for backend failures.
   - Distinguish insufficient evidence from runtime failures.

5. Hosted Smoke Path
   - Add narrow startup and request smoke coverage for the MVP app path.
   - Keep smoke checks operational and lightweight.

6. Validation Coverage
   - Add tests for the UI integration seam, rendering-relevant mapping, and
     failure-state behavior.

7. Deferred Work Boundary
   - Explicitly stop before advanced UI polish, conversation state, and deeper
     observability work.
