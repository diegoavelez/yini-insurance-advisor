# Validation — phase-15-final-test-release-baseline

This slice is ready when the repository exposes one clear MVP final-test
baseline that operators can run before release, instead of inferring it from a
large undifferentiated test surface.

## Checks

- A documented final-test baseline exists for the current MVP.
- The baseline lists exact commands, not only categories of tests.
- The baseline explains which release-critical surface each command protects.
- Broader non-gating suites are explicitly separated from the mandatory gate.
- `Makefile` exposes a minimal `test-release` helper target for the baseline.
- `specs/roadmap.md` records the slice as completed Phase 15 verification work.

## Implemented baseline

- `make test-release`
- `README.md` documents the command as the authoritative deterministic
  pre-release gate.
- `docs/evaluation-report.md` maps each grouped command to its protected MVP
  surface.
- `make test-release` passed locally after pinning the helper to `PYTHONPATH=.`
  for repo-root execution.
