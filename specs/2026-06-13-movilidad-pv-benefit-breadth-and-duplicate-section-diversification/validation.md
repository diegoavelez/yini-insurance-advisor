# Validation

This slice is ready when explicit movilidad PV benefit-intent retrieval favors
broader distinct PV sections and suppresses duplicate repeats from the same
section.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval tests cover the live-style PV ranking scenario.
- Duplicate `Pérdidas totales` chunks no longer occupy multiple early slots.
- Broader PV sections outrank narrow service-detail sections for the general
  benefits query.
- The roadmap records the slice as a narrow intra-PV refinement.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`

## Execution Notes

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q` passed locally.
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
  passed locally.
- A fresh live Qdrant rerun is still recommended to confirm the improved
  breadth ordering on the indexed PV family.

## Expected Outcome

- Queries like `qué beneficios incluye la propuesta de valor de movilidad`
  produce a more varied top-k inside the PV family.
- Narrow sections such as `Grúa de amplio alcance` no longer crowd out broader
  benefit sections when the query is general.
- The slice stops before broader reranker redesign.
