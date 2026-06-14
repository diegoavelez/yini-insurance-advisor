# Plan

## Objective

Run a safe baseline ingestion for the `PV` transversal mobility cohort and
determine whether extraction quality is good enough for downstream retrieval.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-pv-portafolio-baseline-ingestion-and-extraction-audit/requirements.md`
- `specs/2026-06-13-movilidad-pv-portafolio-baseline-ingestion-and-extraction-audit/plan.md`
- `specs/2026-06-13-movilidad-pv-portafolio-baseline-ingestion-and-extraction-audit/validation.md`

## Assumptions

- Metadata overlays already classify both `PV` documents as
  `document_type=guide` and `product=movilidad`.
- Current batch-glob controls are sufficient to target this cohort narrowly.

## Risks

- `PV` documents may be visually rich and generate weak markdown ordering or
  repetitive chunks under the current Docling-first path.

## Verification Strategy

- Run cohort-only ingestion.
- Confirm artifacts exist for both documents.
- Inspect cleaned markdown and the first chunk windows for title/structure
  quality.
- Record whether a remediation slice is needed before embeddings/indexing.
