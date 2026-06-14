# Plan

## Objective

Onboard the single-document `suscripción` transversal cohort with the existing
baseline ingestion/indexing/retrieval seams and capture any first real
retrieval gap as a separate corrective slice.

## Affected Files

- `specs/2026-06-14-movilidad-suscripcion-corpus-baseline-ingestion-and-retrieval/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-corpus-baseline-ingestion-and-retrieval/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-corpus-baseline-ingestion-and-retrieval/validation.md`
- `specs/roadmap.md` if the tracked next-slice wording needs clarification

## Assumptions

- the existing overlay entry for `politicas de suscripcion de movilidad.pdf`
  is already correct;
- the current `product=movilidad` baseline is sufficient for the first pass;
- any retrieval ranking or scope issue should be observed from real retrieval
  before opening a corrective slice.

## Risks

- the suscripción policy may retrieve adjacent mobility commercial or process
  material ahead of underwriting-policy evidence;
- extraction may flatten operational rules or tabular criteria into weak chunk
  surfaces;
- operator runs may accidentally widen the glob beyond the target file.

## Steps

1. Run cohort-only ingestion.
2. Run cohort-only embeddings generation.
3. Run cohort-only Qdrant indexing.
4. Run first suscripción-oriented retrieval checks.
5. Open a narrow corrective slice only if evidence demands it.

## Verification Strategy

- verify the exact glob remains cohort-local;
- inspect the manifests and artifacts for the suscripción document;
- validate one or more suscripción-style retrieval queries.
