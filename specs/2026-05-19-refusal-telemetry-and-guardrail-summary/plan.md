# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Telemetry Surface Definition
   - Define the narrow local surface for reviewing guardrail/refusal events.
   - Keep it deterministic and compact.

2. Guardrail Event Aggregation
   - Aggregate already-emitted guardrail/refusal events by type.
   - Preserve request correlation where available.

3. Summary Output
   - Expose a typed summary of counts and recent event context.
   - Keep the output operational rather than analytical.

4. Validation Coverage
   - Add tests for summary correctness across multiple guardrail types.
   - Add tests for request-correlation preservation where available.
