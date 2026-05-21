# Plan

## Status

- Completed.

1. Trace Surface
   - Add a narrow trace-summary display to the current demo UI.
   - Reuse existing seams where possible.

2. Presentation
   - Keep the trace concise and review-oriented.
   - Avoid broader debug-context work in this slice.

3. Validation
   - Add deterministic validation for the trace-summary surface.
   - Confirm the slice stops before debug-context exposure.

## Notes

- Added a narrow `Trace Summary` output to the Gradio `Blocks` UI.
- Kept the trace review-oriented by deriving a short summary from the current
  grounded result and honoring an explicit `trace_summary` seam when present.
- Stopped before broader debug-context, loading/error-state, or degraded-service
  work.
