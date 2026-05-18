# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- Default settings load with `deployment_mode="public_mvp_demo"`.
- Environment overrides can set `DEPLOYMENT_MODE=internal_production`.
- Invalid deployment-mode values fail validation.
- Default startup remains valid in public MVP demo mode.
- `APP_ENV` accepted values are explicit: `development`, `test`, `staging`,
  `production`.
- `internal_production` fails startup validation when `APP_ENV=development`.
- `internal_production` passes startup validation when `APP_ENV` is `test`,
  `staging`, or `production`.

## Merge Readiness

This slice is ready when deployment mode is part of the typed config contract
and the new startup distinction is fully covered by tests.
