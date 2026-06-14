# Validation

This slice is ready when explicit ARL account-update answers no longer cite the
lateral commissions guide.

## Acceptance Checks

- The new spec bundle exists.
- Focused grounded-answer coverage proves only the account-update guide remains
  in answer-facing evidence for the narrow query family.
- Live `answer-query` for the account-update guide query returns only the
  account-update guide in `documentary_basis` and `citations`.

## Baseline Gap Evidence

- Live `answer-query` for
  `¿Cómo actualizo la cuenta bancaria para pago de comisiones ARL?` currently
  cites:
  - `Actualización de cuenta bancaria para pago de comisiones ARL SURA`
  - `Consulta liquidación de comisiones para intermediarios de Riesgos Laborales`

## Completion Evidence

- Focused grounded-answer coverage passes with:
  `./.venv/bin/python -m pytest tests/test_grounded_answer_generation.py -q -k 'arl_commissions or arl_account_update or arl_rui or financing_evidence'`
- Static verification passes with:
  `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_grounded_answer_generation.py`
- Live `answer-query` validation succeeds with:
  `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cómo actualizo la cuenta bancaria para pago de comisiones ARL?' --product arl --document-type guide --top-k 3`
- The live account-update answer now completes with `confidence = high` and
  `citation_count = 1`.
- The live `documentary_basis` and `citations` now contain only:
  `Actualización de cuenta bancaria para pago de comisiones ARL SURA`

## Follow-on Gap

- The next narrow ARL quality gap is now in the remuneration policy chunk
  surface: the current `Canal Externo ARL V1 Esquema remuneración y políticas
  que lo complementan` chunks still carry duplicated heading prefixes such as
  repeated `## Canales para la afiliación a ARL SURA`, which weakens retrieval
  readability without blocking the operational path.
- The next narrow corrective slice is therefore
  `arl-remuneracion-policy-heading-dedup`.
