# Requirements

## Feature Summary

This feature closes the last identified gap in `Phase 1 — Configuration and
Contracts` by adding explicit deployment mode flags to `core.config.Settings`.

The goal is to model the constitution's dual deployment posture directly in the
typed settings layer:

- `public_mvp_demo`
- `internal_production`

## In Scope

- Add a typed deployment-mode field to `core.config.Settings`.
- Add validation for accepted deployment-mode values.
- Add the minimum startup validation behavior needed to keep
  `internal_production` distinct from the default public MVP demo posture.
- Update `.env.example` to document the new settings contract.
- Add tests for valid and invalid deployment-mode behavior.

## Out of Scope

- Authentication rules.
- Provider-specific branching logic.
- UI behavior differences.
- Access control.
- Deployment platform wiring.

## Decisions

### Allowed Values

The deployment mode field should be restricted to:

- `public_mvp_demo`
- `internal_production`

### Default

The default must be `public_mvp_demo`, because the current MVP posture is a
publicly accessible demo even though the long-term production target is
internal-only.

### Startup Behavior

`public_mvp_demo` should remain valid with the current default local startup
path.

`internal_production` should require a non-development app environment at
startup so it cannot be treated as a casual local default.

For this slice, the allowed `APP_ENV` values remain:

- `development`
- `test`
- `staging`
- `production`

For deployment-mode validation purposes:

- `development` is valid only with `public_mvp_demo`;
- `test`, `staging`, and `production` are valid with either deployment mode;
- `internal_production` must reject `APP_ENV=development`.

This slice should not add any provider or secret requirements beyond the
existing startup validation seam.

## Acceptance Criteria

- `core.config.Settings` exposes a typed deployment-mode field.
- Invalid deployment-mode values fail loudly.
- Default startup still succeeds in `public_mvp_demo`.
- `internal_production` with `APP_ENV=development` fails startup validation.
- `internal_production` with a non-development app environment passes startup
  validation if no other existing requirements are violated.
