# Validation

## Merge Readiness Checks

The feature is ready to merge only if configuration behavior is correct and the
validation rules are enforced through automated tests.

## Required Automated Checks

- `ruff check .`
- `pytest`

These checks must run under a supported Python 3.11+ environment.

## Required Test Scenarios

### Settings Parsing

- Default settings load successfully with no `.env` file required.
- Environment overrides map correctly onto the typed settings fields.
- Invalid `APP_ENV` values fail validation.
- Invalid `LOG_LEVEL` values fail validation.
- `MAX_INPUT_CHARS` rejects zero, negative values, and values above the allowed
  bound.
- `TOP_K` rejects zero, negative values, and values above the allowed bound.
- Blank strings for optional string fields normalize to `None`.

### Startup Validation

- Minimal local startup succeeds without requiring Groq, Qdrant, or Phoenix
  credentials.
- Startup validation uses one centralized entry point.
- Startup validation produces actionable failures for invalid configuration.
- Cached settings access remains stable and does not require duplicate env
  parsing in runtime code.

### App Integration

- The app entry point performs startup validation before continuing.
- The app still starts successfully for the local scaffold path.
- Failure messaging is explicit enough to identify the invalid setting or
  missing requirement.

## Manual Smoke Checks

- Run the app entry point in a clean local environment and confirm successful
  startup with Phase 1 defaults.
- Run the app entry point with at least one intentionally invalid environment
  value and confirm it fails loudly with actionable messaging.
- Confirm `.env.example` and README instructions still match the actual settings
  contract after implementation.

## Non-Goals for Validation

- Do not require live Groq, Qdrant, or Phoenix credentials in this feature.
- Do not add retrieval, tool, response, or workflow contract checks in this
  slice.
