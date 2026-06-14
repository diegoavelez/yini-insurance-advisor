# Plan

## Objective

Reduce noisy repetition and improve semantic chunk density for the two
transversal `PV` mobility documents.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-pv-structure-and-chunk-dedup-remediation/requirements.md`
- `specs/2026-06-13-movilidad-pv-structure-and-chunk-dedup-remediation/validation.md`

## Assumptions

- The current ingestion output is structurally close enough that a narrow
  normalization pass can improve it without introducing OCR-specific logic.

## Risks

- If applicability-block merging is too broad, unrelated sections could be
  fused and reduce citation precision.

## Verification Strategy

- Add focused tests for PV block normalization and applicability-block pairing.
- Rebuild the two `PV` artifacts.
- Compare chunk counts and inspect leading chunks for better structure.
