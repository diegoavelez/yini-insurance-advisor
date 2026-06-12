# Plan

## Objective

Prevent obviously noisy media/embed headings from becoming retrieval-facing
document titles.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `README.md`
- `specs/roadmap.md`
- `specs/2026-06-12-noisy-document-title-heading-guardrail/requirements.md`
- `specs/2026-06-12-noisy-document-title-heading-guardrail/validation.md`

## Assumptions

- the deterministic filename stem is preferable to a noisy extracted heading;
- a narrow guardrail is safer than broader title inference for the current
  corpus stage;
- ARL FAQ documents are representative of this specific failure mode.

## Risks

- over-filtering legitimate headings that include media-related words;
- implying broader title quality guarantees than the implementation provides;
- mixing this corrective slice with unrelated metadata enrichment.

## Verification Strategy

- add focused ingestion tests for noisy-heading rejection;
- run targeted ingestion lint and tests;
- document the guardrail as a narrow corrective behavior.
