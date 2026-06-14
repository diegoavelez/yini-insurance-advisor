# Plan

## Objective

Improve the suscripción policy extraction surface so live retrieval uses
semantic underwriting-policy sections instead of weak `Page N` fallback chunks.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-suscripcion-corpus-baseline-ingestion-and-retrieval/validation.md`
- `specs/2026-06-14-movilidad-suscripcion-section-structure-remediation/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-section-structure-remediation/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-section-structure-remediation/validation.md`

## Assumptions

- the current family scoping is already correct;
- the main quality loss comes from page-level PDFium fallback structure rather
  than embedding/indexing failure;
- targeted normalization for this policy shape is sufficient before considering
  broader retrieval heuristics.

## Risks

- over-normalizing numbered policy headings and losing important context;
- removing boilerplate too aggressively and dropping real policy content;
- improving the cleaned surface without materially improving live retrieval.

## Steps

1. Inspect the fallback-generated suscripción cleaned markdown and leading chunks.
2. Add the smallest document-shape normalization that suppresses page
   boilerplate and promotes semantic section labels.
3. Regenerate the suscripción artifacts and rerun live retrieval.
4. Record the outcome and any remaining narrow gap.

## Verification Strategy

- inspect the normalized cleaned markdown head;
- inspect regenerated chunk sections;
- rerun the two live suscripción retrieval queries.
