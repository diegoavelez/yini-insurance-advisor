# Validation

This slice is ready when `MOTOS` comparison-intent queries activate the
existing comparison retrieval path through a narrow operator-curated rule.

## Acceptance Checks

- The spec bundle exists.
- `ops/term-equivalences.json` contains a `motos` comparison rule.
- Focused retrieval regression coverage passes.
- The real comparison retrieval query is rerun.
- The real comparison answer query is rerun.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
- `./.venv/bin/python -m ruff check tests/test_retrieval.py`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué diferencias hay entre los planes de motos?' --top-k 12 --product moto`
- `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué diferencias hay entre los planes de motos?' --top-k 5 --product moto`

## Follow-on Rule

If `comparativo motos.pdf` still fails to surface prominently after this slice,
the next slice should target comparative artifact representation or chunk
normalization, not broader retrieval-policy drift.
