# Plan

## Objective

Onboard `MOVILIDAD/VIAJES` into the canonical RAG pipeline with the smallest
truthful baseline: metadata support, ingestion, embeddings, indexing, and first
retrieval validation.

## Affected files

- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json`
- `core/query_scope.py`
- `tests/test_ingestion.py`
- `tests/test_retrieval.py`
- `tests/test_query_scope.py`
- `specs/roadmap.md`

## Assumptions

- the four PDFs currently present in `data/raw/MOVILIDAD/VIAJES/` are the
  intended initial category corpus;
- `ayudaventas` should be classified as `guide` and `clausulado` as `policy`;
- no category-specific reranking is needed until live retrieval reveals a
  concrete gap.

## Risks

- the English `ayudaventas` guide may later compete with the Spanish guide for
  broad commercial-intent queries;
- without a follow-on corrective slice, broad `viajes` benefit queries may need
  later family scoping or diversification;
- onboarding commands must stay tightly scoped so they do not reopen the wider
  movilidad corpus.

## Execution

1. Add canonical `viajes` aliases and overlays.
2. Add focused coverage for product inference, overlays, retrieval filter
   canonicalization, and query scope.
3. Update the roadmap and create this spec bundle.
4. Run ingestion, embeddings, indexing, and first retrieval validation only for
   `MOVILIDAD/VIAJES/`.

## Verification strategy

- run focused `pytest` checks for ingestion, retrieval, and query scope;
- verify the live onboarding commands succeed only for `VIAJES` artifacts;
- record any ranking gap as a new corrective slice instead of broadening this
  baseline spec.
