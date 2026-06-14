# Validation

This slice is ready when explicit movilidad PV benefit-intent queries are
scoped to the `PROPUESTA DE VALOR MOVILIDAD` document family through the
existing curated filter seam.

## Acceptance Checks

- The new spec bundle exists.
- `ops/term-equivalences.json` includes a PV-specific `document_name` query filter rule.
- Focused retrieval tests prove the normalized query carries the PV document-name filter.
- Focused retrieval tests prove local lexical candidates from non-PV mobility guides are excluded.
- The roadmap records the new narrow corrective slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
- `./.venv/bin/python -m ruff check tests/test_retrieval.py`
- `./.venv/bin/python -m json.tool ops/term-equivalences.json`

## Execution Notes

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q` passed locally.
- `./.venv/bin/python -m ruff check tests/test_retrieval.py` passed locally.
- `./.venv/bin/python -m json.tool ops/term-equivalences.json` passed locally.
- Live Qdrant rerun remains operator-executed because this harness cannot
  reliably perform the external retrieval check.

## Expected Outcome

- Queries like `qué beneficios incluye la propuesta de valor de movilidad`
  remain within the PV document family by default.
- Adjacent mobility guides with overlapping benefit anchors no longer crowd the
  top results for this specific intent.
- The slice stops before broader reranker redesign or new metadata schema work.
