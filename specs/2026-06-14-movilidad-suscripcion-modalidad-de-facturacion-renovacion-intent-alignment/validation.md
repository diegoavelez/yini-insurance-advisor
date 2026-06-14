# Validation

This slice is ready when renewal-specific collective billing queries foreground
`14.6.2` collective-policy evidence instead of individual payment-change rules.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval coverage proves `14.6.2` outranks `13.10` / `13.1.2` for the
  documented query pattern.
- At least one live `answer-query` run for the documented renewal question keeps
  `supported=true` while foregrounding collective-policy evidence.

## Baseline Gap Evidence

- Live retrieval for
  `¿Se puede cambiar la modalidad de facturación en la renovación de una póliza colectiva?`
  currently ranks `13.10. Cambio en forma de pago negocio individual` and
  `13.1.2. Cambio de Plan de Pagos Anual Financiado` ahead of the collective
  `14.6.2` billing section.
- The live answer is directionally correct, but its leading documentary basis
  and citations are still anchored in individual-plan-change sections rather
  than the collective-policy evidence that directly answers the question.

## Completion Evidence

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'renewal or asegurado or collective_billing'`
  passed after adding the narrow renewal-specific collective billing reranking
  regression.
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
  passed.
- Live retrieval for
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Se puede cambiar la modalidad de facturación en la renovación de una póliza colectiva?' --product movilidad --document-type policy --top-k 5`
  now returns
  `movilidad__transversales__politicas-de-suscripcion-de-movilidad:v2:0111`
  first.
- Live grounded answering for
  `./.venv/bin/python -m rag.ingestion answer-query --query '¿Se puede cambiar la modalidad de facturación en la renovación de una póliza colectiva?' --product movilidad --document-type policy --top-k 5`
  still returns `supported=true`, and its leading documentary basis now starts
  with the collective-policy `14.6.2` evidence instead of individual-plan-change
  sections.
