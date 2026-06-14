# Plan

## Objective

Onboard the single-document `financiación` transversal cohort with the existing
baseline ingestion/indexing/retrieval seams and capture any first real
retrieval gap as a separate corrective slice.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-financiacion-corpus-baseline-ingestion-and-retrieval/requirements.md`
- `specs/2026-06-14-movilidad-financiacion-corpus-baseline-ingestion-and-retrieval/plan.md`
- `specs/2026-06-14-movilidad-financiacion-corpus-baseline-ingestion-and-retrieval/validation.md`

## Assumptions

- the existing overlay entry for `instructivo financiacion de polizas v1.pdf`
  is already correct;
- the current `product=movilidad` baseline is sufficient for the first pass;
- any ranking or structure issue should be observed from real retrieval before
  opening a corrective slice.

## Risks

- the financing guide may retrieve broader mobility commercial material ahead
  of procedural financing evidence;
- Docling extraction may flatten lists or steps that later need structuring;
- operator runs may accidentally widen the glob beyond the target file.

## Steps

1. Run cohort-only ingestion.
2. Run cohort-only embeddings generation.
3. Run cohort-only Qdrant indexing.
4. Run first financing-oriented retrieval checks.
5. Open a narrow corrective slice only if evidence demands it.

## Verification Strategy

- verify the exact glob remains cohort-local;
- inspect the manifests/artifacts for the financing document;
- validate one or more financing-style retrieval queries.
