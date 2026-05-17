# Requirements

## Feature Summary

This feature defines the first implementation slice of `Phase 1 — Configuration
and Contracts` from `specs/roadmap.md`.

The goal is to harden `core.config.Settings` into the single typed
configuration boundary for the application and add explicit startup validation
that fails loudly with actionable errors.

This slice follows the guidance in `specs/mission.md` and `specs/tech-stack.md`
to keep the system:

- explicit;
- typed;
- small in scope;
- testable;
- production-oriented without premature abstraction.

## User and System Need

Before building ingestion, retrieval, or agent workflows, the repository needs
a trustworthy configuration layer so future modules can:

- read configuration through one contract;
- reject invalid values early;
- avoid duplicating environment parsing logic;
- surface boot-time misconfiguration clearly.

## In Scope

- Strengthen `core.config.Settings` as the only public settings model.
- Define the baseline environment contract using the PRD variables:
  - `GROQ_API_KEY`
  - `GROQ_MODEL`
  - `QDRANT_URL`
  - `QDRANT_API_KEY`
  - `QDRANT_COLLECTION`
  - `EMBEDDING_PROVIDER`
  - `EMBEDDING_MODEL`
  - `PHOENIX_PROJECT_NAME`
  - `PHOENIX_ENDPOINT`
  - `APP_ENV`
  - `LOG_LEVEL`
  - `MAX_INPUT_CHARS`
  - `TOP_K`
- Normalize blank strings consistently for optional string settings.
- Enforce enum and numeric validation through Pydantic.
- Add explicit startup validation so app boot can validate configuration beyond
  raw parsing.
- Define when provider-specific credentials become required.
- Ensure future modules consume cached settings instead of reading env vars
  directly.
- Update docs and `.env.example` only if the settings contract changes.

## Out of Scope

- Retrieval contracts.
- Tool contracts.
- Response contracts.
- Workflow state contracts.
- Qdrant client initialization.
- Groq client initialization.
- Phoenix instrumentation.
- Subsystem runtime wiring beyond validation rules.

## Baseline Decisions

### Settings Boundary

`core.config.Settings` remains the only public settings type. Future modules
must obtain configuration through `get_settings()` or a thin replacement built
around the same cached boundary.

### Validation Split

Separate validation into two layers:

1. parse-time validation handled by Pydantic field types and validators;
2. startup validation handled by one explicit application-facing validation
   entry point.

This keeps environment parsing reusable while allowing stricter boot rules as
features are enabled later.

### Optional vs Required Values in This Slice

For Phase 1 startup, only generic app configuration must be valid by default.

- `APP_ENV`, `LOG_LEVEL`, `MAX_INPUT_CHARS`, and `TOP_K` must always validate.
- `GROQ_MODEL`, `QDRANT_COLLECTION`, `EMBEDDING_PROVIDER`,
  `EMBEDDING_MODEL`, and `PHOENIX_PROJECT_NAME` may retain defaults.
- `GROQ_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, and `PHOENIX_ENDPOINT` remain
  optional during bare startup because the related providers are not yet used.

Provider-specific secrets become required only when the corresponding subsystem
or provider is explicitly enabled by future features.

### Startup Validation Seam

Add one explicit startup validation seam centralized in `core.config`, either:

- `Settings.validate_startup()`, or
- `validate_startup_settings(settings: Settings)`.

It must:

- return successfully for a minimal local Phase 1 boot;
- raise clear validation errors for invalid environment shape;
- be the single place where future subsystem-required checks are added.

### Future Access Pattern

Future modules should not instantiate `Settings()` directly unless they are
tests specifically verifying parse behavior. Runtime code should use
`get_settings()` so caching and validation policy stay centralized.

## Acceptance Criteria

- `core.config.Settings` remains typed and is the only settings contract.
- Invalid enum values fail loudly.
- Invalid numeric bounds fail loudly.
- Blank strings for optional string settings normalize to `None`.
- Minimal local startup works without forcing unused provider credentials.
- Boot-time validation exists and can be called explicitly by the app entry
  point.
- The validation seam is written so future provider checks can be added without
  duplicating env access logic.
- Tests cover both parsing and startup validation outcomes.

## Constraints and Guidance

- Follow `specs/mission.md`: explicit contracts, small iterations, and fail
  loud behavior.
- Follow `specs/tech-stack.md`: Pydantic v2, structured logging, Python 3.11+,
  and no hidden mutable state.
- Do not broaden this feature into shared business-domain schemas.
