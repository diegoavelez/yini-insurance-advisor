# Plan

## Status

- Completed.

1. Debug Surface
   - Add a narrow debug-metadata display to the current demo UI.
   - Reuse existing seams where possible.

2. Presentation
   - Keep the debug metadata compact and operationally useful.
   - Preserve clear separation from the user-visible support context.

3. Validation
   - Add deterministic validation for the debug-metadata surface.
   - Confirm the slice stops before loading/error-state work.

## Notes

- Added a narrow `Debug Metadata` surface to the current Gradio UI.
- Reused current request-correlation and result seams to expose compact
  operator-facing metadata without reopening the user-visible support surface.
- Stopped before loading-state, error-state, and degraded-service work.
