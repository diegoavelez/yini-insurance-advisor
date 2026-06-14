# Plan

## Objective

Determine whether the current transversal mobility `PV` artifacts are good
enough for embeddings/indexing, or whether one more narrow cleanup slice is the
safer move.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-pv-retrieval-readiness-audit/requirements.md`
- `specs/2026-06-13-movilidad-pv-retrieval-readiness-audit/validation.md`

## Assumptions

- The latest `PV` chunk artifacts in `data/processed/chunks/` reflect the
  current code and can be used as the source of truth for readiness.

## Risks

- Local embedding generation may fail for environmental reasons unrelated to
  corpus quality, so the audit must separate content readiness from runtime
  network/cache readiness.

## Verification Strategy

- Measure duplicate chunk surfaces, applicability density, and merged evidence.
- Attempt local embedding generation for the `PV` chunk artifacts.
- Record whether the final outcome is `go` or `no-go` and why.
