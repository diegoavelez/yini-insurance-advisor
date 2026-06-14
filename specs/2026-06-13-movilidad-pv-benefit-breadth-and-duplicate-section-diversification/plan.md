# Plan

## Objective

Improve explicit movilidad PV benefit-intent retrieval by preferring broader
distinct PV benefit sections and suppressing duplicate section repeats.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-pv-benefit-breadth-and-duplicate-section-diversification/requirements.md`
- `specs/2026-06-13-movilidad-pv-benefit-breadth-and-duplicate-section-diversification/validation.md`

## Assumptions

- the remaining issue is ranking quality within the PV family, not recall or scope;
- section-level duplication can be handled with a deterministic local post-pass;
- broader sections can be approximated from text structure without adding new metadata.

## Risks

- over-diversifying and hiding the strongest section;
- applying PV-specific breadth logic to unrelated retrieval flows;
- overfitting the score to current examples.

## Steps

1. Add a narrow PV benefit-intent detector.
2. Add deterministic breadth scoring and per-section dedup for PV results.
3. Add focused tests reproducing the live PV ranking issue.
4. Update the roadmap and validation notes.
5. Run targeted tests and lint.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- ask for one operator rerun if a fresh live confirmation is needed.
