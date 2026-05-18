# Plan

1. Settings Contract
   - Add a typed deployment-mode field to `core.config.Settings`.
   - Keep the value set limited to `public_mvp_demo` and
     `internal_production`.

2. Startup Validation
   - Extend the centralized startup validation seam with the minimum
     deployment-mode rule.
   - Preserve all current provider-related startup behavior.

3. Documentation Alignment
   - Add the new environment variable to `.env.example`.
   - Keep the change limited to the config contract surface.

4. Tests
   - Add tests for default mode, env overrides, invalid values, and startup
     behavior differences for `internal_production`.
