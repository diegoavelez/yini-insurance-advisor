# Validation

This slice is ready when movilidad PV benefit-intent queries activate a narrow
curated expansion bundle and deterministic reranking can favor the expected PV
benefit sections over weaker lateral evidence.

## Acceptance Checks

- The new spec bundle exists.
- A curated PV benefit-intent expansion rule exists in
  `ops/term-equivalences.json`.
- Focused retrieval tests prove the query is augmented with PV benefit anchors.
- Focused retrieval tests prove PV benefit sections can outrank weaker generic
  or lateral guide hits.
- The roadmap records the slice as a narrow retrieval-alignment correction.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
- `./.venv/bin/python -m ruff check tests/test_retrieval.py`

## Execution Notes

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q` passed locally.
- `./.venv/bin/python -m ruff check tests/test_retrieval.py` passed locally.
- `./.venv/bin/python -m json.tool ops/term-equivalences.json` passed locally.

## Expected Outcome

- Queries such as `qué beneficios incluye la propuesta de valor de movilidad`
  reuse the existing candidate-pool widening and reranking seam through a new
  curated rule.
- Relevant PV evidence such as `Viajes` or `Pérdidas totales` can surface ahead
  of `Canales de atención` and unrelated mobility-guide chunks.
- The slice stops before broader reranker design, new metadata filters, or Qdrant
  contract changes.
