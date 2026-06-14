# Validation

This slice is ready when explicit ARL commissions guide answers no longer cite
the lateral account-update guide.

## Acceptance Checks

- The new spec bundle exists.
- Focused grounded-answer coverage proves only the commissions guide remains in
  answer-facing evidence for the narrow query family.
- Live `answer-query` for the commissions guide query returns only the
  commissions guide in `documentary_basis` and `citations`.

## Baseline Gap Evidence

- Live `answer-query` for `¿Cómo consulto la liquidación de comisiones ARL?`
  currently cites:
  - `Consulta liquidación de comisiones para intermediarios de Riesgos Laborales`
  - `Actualización de cuenta bancaria para pago de comisiones ARL SURA`

## Completion Evidence

- Focused grounded-answer coverage passes with:
  `./.venv/bin/python -m pytest tests/test_grounded_answer_generation.py -q -k 'arl_commissions or arl_rui or financing_evidence'`
- Static verification passes with:
  `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_grounded_answer_generation.py`
- Live `answer-query` validation succeeds with:
  `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cómo consulto la liquidación de comisiones ARL?' --product arl --document-type guide --top-k 3`
- The live commissions answer now completes with `confidence = high` and
  `citation_count = 1`.
- The live `documentary_basis` and `citations` now contain only:
  `Consulta liquidación de comisiones para intermediarios de Riesgos Laborales`

## Follow-on Gap

- Live `answer-query` for the symmetric guide query
  `¿Cómo actualizo la cuenta bancaria para pago de comisiones ARL?` still cites
  the lateral commissions guide as secondary evidence even though the account
  update guide already fully answers the request.
- The next narrow corrective slice is therefore
  `arl-cuenta-bancaria-guide-family-answer-evidence-alignment`.
