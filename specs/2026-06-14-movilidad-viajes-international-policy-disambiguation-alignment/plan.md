# Plan

## Objective

Correct the explicit national-vs-international policy disambiguation gap inside
the new `VIAJES` category.

## Affected files

- likely `ops/term-equivalences.json`
- likely `tests/test_retrieval.py`
- `specs/roadmap.md`

## Assumptions

- the current baseline artifacts and metadata are correct;
- the gap is retrieval-family alignment, not ingestion corruption;
- a narrow curated filter or deterministic reranking bias should be sufficient.

## Risks

- overly aggressive scoping could suppress useful broad viajes-policy results;
- a one-sided fix for `internacional` could leave `nacional` asymmetric.

## Verification strategy

- add focused retrieval tests for explicit `internacional` and `nacional`
  policy queries;
- rerun the live queries against Qdrant after the corrective change.
