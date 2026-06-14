# Plan

## Objective

Remove the remaining `PV` applicability duplication and inline-commercial-tail
noise without widening chunking behavior for other document families.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-pv-applicability-collapse-and-inline-tail-remediation/requirements.md`
- `specs/2026-06-13-movilidad-pv-applicability-collapse-and-inline-tail-remediation/validation.md`

## Assumptions

- The remaining `PV` noise is local to applicability-heavy slide flows and can
  be handled with section-aware overlap control plus narrow body normalization.

## Risks

- If applicability overlap control is too broad, other corpora could lose useful
  continuity across chunk boundaries.

## Verification Strategy

- Add focused unit regressions for overlap suppression and heading-prefixed body
  cleanup.
- Rebuild the two `PV` artifacts.
- Recount `PLANES QUE APLICA` chunks and verify that inline slogan tails no
  longer appear in chunk artifacts.
