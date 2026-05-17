# Plan

1. Config Contract Refinement
   - Review `core.config.Settings` against the PRD environment variable list.
   - Keep `Settings` as the single public configuration contract.
   - Tighten field definitions, defaults, bounds, and blank-string handling only
     where the Phase 1 scope requires it.

2. Startup Validation Design
   - Add one explicit startup validation seam inside `core.config`.
   - Split pure parsing rules from boot-time policy checks so both can evolve
     independently.
   - Define Phase 1 startup as valid without Groq, Qdrant, or Phoenix secrets
     unless a future feature explicitly enables those subsystems.

3. Runtime Access Pattern
   - Preserve `get_settings()` as the central cached access path for runtime
     code.
   - Document that future modules should request settings through the cached
     accessor instead of constructing `Settings()` directly.
   - Ensure the app entry point uses the centralized validation seam during
     startup.

4. Test Coverage
   - Add unit tests for defaults, environment overrides, enum validation,
     numeric bounds, and blank-string normalization.
   - Add tests for startup validation success with minimal local config.
   - Add tests for startup validation failures when configuration is invalid or
     when a future-facing provider-specific requirement is explicitly triggered.

5. Docs and Contract Alignment
   - Update `.env.example` only if the effective Phase 1 contract changes.
   - Update README setup or configuration notes only if startup expectations
     change.
   - Keep the feature scoped to settings and env validation; defer shared
     contracts to the next Phase 1 spec.
