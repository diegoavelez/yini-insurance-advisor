# Plan

## Objective

Repair inconsistent subsection numbering inside the suscripción collective
policies section while preserving current retrieval quality.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-suscripcion-breadth-diversification/validation.md`
- `specs/2026-06-14-movilidad-suscripcion-subsection-lineage-normalization/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-subsection-lineage-normalization/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-subsection-lineage-normalization/validation.md`

## Assumptions

- the current ranking behavior is good enough to preserve;
- the remaining issue comes from heading normalization rather than retrieval;
- the problematic headings are localized enough for a narrow fix.

## Risks

- accidentally rewriting correct numbered headings elsewhere in the document;
- improving collective-policy lineage while breaking chunk section paths;
- overfitting to one subsection pattern and missing sibling cases.

## Steps

1. Capture the inconsistent collective-policy headings in cleaned markdown.
2. Add the smallest heading-lineage normalization needed.
3. Add focused ingestion and retrieval regression coverage.
4. Rebuild suscripción artifacts and recheck live retrieval labels.

## Verification Strategy

- run focused ingestion and retrieval tests;
- run Ruff on touched files;
- rerun suscripción ingestion for this document;
- rerun at least one live suscripción retrieval query.
