# Plan

## Objective

Open the first narrow retrieval path for `choque simple` questions using the
shared mobility transversal corpus.

## Affected Files

- `core/query_scope.py`
- `ops/term-equivalences.json`
- `tests/test_query_scope.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-choque-simple-supported-scope-and-retrieval/requirements.md`
- `specs/2026-06-13-movilidad-choque-simple-supported-scope-and-retrieval/validation.md`

## Assumptions

- `choque simple` is the first transversal mobility intent worth opening.
- `guide` is the right first retrieval surface for this corpus family.

## Risks

- A broad `choque simple` bundle could over-match unrelated accident queries if
  kept too generic.
- The `ley 2251` source may later deserve a more specific taxonomy than
  `guide`, but that is intentionally deferred.

## Verification Strategy

- Add focused query-scope and retrieval tests.
- Run focused `pytest` and `ruff`.
- Leave broader ingestion/indexing of the remaining transversal documents for
  the operational batch workflow.
