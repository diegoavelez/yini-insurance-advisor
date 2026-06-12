# Plan

## Objective

Add a narrow operator-curated equivalence seam for retrieval normalization.

## Affected Files

- `contracts/ingestion.py`
- `contracts/__init__.py`
- `rag/ingestion.py`
- `ops/term-equivalences.json`
- `README.md`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-12-operator-curated-term-equivalence-normalization/requirements.md`
- `specs/2026-06-12-operator-curated-term-equivalence-normalization/validation.md`

## Assumptions

- deterministic operator curation is preferable to automatic synonym inference;
- retrieval-time normalization is enough for the current scope;
- canonical values should remain operator-defined so they can match current
  metadata overlays.

## Risks

- over-expanding query text with low-value aliases;
- drifting canonical values away from metadata overlay values;
- broadening scope into taxonomy redesign.

## Verification Strategy

- add focused retrieval tests for query expansion and filter canonicalization;
- verify existing retrieval behavior remains intact for unaffected cases;
- document how operators should maintain the table.
