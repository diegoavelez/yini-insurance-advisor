# Plan

## Objective

Onboard the `utilitarios y pesados` transversal cohort with the existing
baseline ingestion/indexing/retrieval seams and capture any first real
retrieval gap as a separate corrective slice.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-utilitarios-pesados-corpus-baseline-ingestion-and-retrieval/requirements.md`
- `specs/2026-06-14-movilidad-utilitarios-pesados-corpus-baseline-ingestion-and-retrieval/plan.md`
- `specs/2026-06-14-movilidad-utilitarios-pesados-corpus-baseline-ingestion-and-retrieval/validation.md`

## Assumptions

- the existing overlay entries for this cohort are already correct;
- the current `product=movilidad` baseline is sufficient for the first pass;
- any ranking or structure issue should be observed from real retrieval before
  opening a corrective slice.

## Risks

- the cohort may mix commercial guide language with policy language in a way
  that needs later document-type or intent alignment;
- clause-heavy policy retrieval may surface broader transversal noise before a
  cohort-specific seam exists;
- operator runs may accidentally widen the glob beyond the two target files.

## Steps

1. Run cohort-only ingestion.
2. Run cohort-only embeddings generation.
3. Run cohort-only Qdrant indexing.
4. Run first guide/policy retrieval checks.
5. Open a narrow corrective slice only if evidence demands it.

## Verification Strategy

- verify the exact globs remain cohort-local;
- inspect the manifests/artifacts for both documents;
- validate one guide-style and one policy-style retrieval query.
