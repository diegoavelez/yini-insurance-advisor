# Plan

## Objective

Remove exact duplicated standalone applicability chunks from the `PV`
portafolio corpus without broadening deduplication to the rest of the system.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-pv-duplicate-applicability-dedup-remediation/requirements.md`
- `specs/2026-06-13-movilidad-pv-duplicate-applicability-dedup-remediation/validation.md`

## Assumptions

- The remaining duplicate risk is limited to exact repeated standalone
  `PLANES QUE APLICA` chunks inside `pv portafolio movilidad v2`.

## Risks

- If the deduplication scope is too broad, legitimate repeated evidence across
  distinct semantic sections could be dropped.

## Verification Strategy

- Add focused unit coverage for exact standalone applicability dedup.
- Rebuild the `PV` cohort.
- Recount duplicate groups and applicability-chunk density.
