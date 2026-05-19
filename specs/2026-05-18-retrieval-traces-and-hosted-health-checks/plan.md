# Plan

## Status

- Completed on `2026-05-18`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Trace Surface
   - Extend the current structured event model with explicit latency traces.
   - Keep retrieval and grounded-answer timing correlated to request ids.

2. Hosted Health Contract
   - Define the narrow health signal for the current app process.
   - Keep it operational and minimal.

3. Hosted Readiness Contract
   - Define readiness checks for current MVP dependencies and configuration.
   - Keep readiness aligned to the real grounded QA serving path.

4. Phoenix Activation
   - Add optional Phoenix activation when configured.
   - Preserve clean behavior when Phoenix is absent or disabled.

5. Failure Policy
   - Make readiness and Phoenix failure behavior explicit and testable.
   - Keep failures structured and diagnosable.

6. Validation Coverage
   - Add tests for latency trace emission, health/readiness behavior, and
     conditional Phoenix activation.

7. Deferred Work Boundary
   - Stop before dashboards, deep metrics, or broader observability expansion.
