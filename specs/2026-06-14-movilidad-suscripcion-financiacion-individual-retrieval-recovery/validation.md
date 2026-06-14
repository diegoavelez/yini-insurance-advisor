# Validation

This slice is ready when suscripción financing-individual queries recover the
existing `13.11` evidence instead of returning zero chunks.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval coverage proves `13.11` evidence is recovered for the
  documented financing query pattern.
- At least one live `retrieve-chunks` run for the documented query returns
  suscripción `13.11` evidence.
- At least one live `answer-query` run for the documented query grounds its
  answer in `13.11` evidence.

## Baseline Gap Evidence

- Live retrieval for
  `¿Cómo funciona la financiación de pólizas individuales en movilidad?`
  currently returns zero chunks.
- The current local suscripción chunk artifact already contains the relevant
  `13.11. Financiación de Pólizas Individuales` chunks, so the gap is retrieval
  recovery rather than ingestion absence.

## Recovery Evidence

- Focused regression coverage now proves that supported suscripción financing
  queries skip the conflicting `document_name` injection and recover `13.11`
  evidence with `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k
  'financing or renewal or asegurado or collective_billing or
  normalize_query_skips_document_name'`.
- Static verification passes with
  `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`.
- Live retrieval with
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo funciona la financiación de pólizas individuales en movilidad?' --product movilidad --document-type policy --top-k 5`
  now returns `movilidad__transversales__politicas-de-suscripcion-de-movilidad:v2:0095`
  first, under section `13.11. Financiación de Pólizas Individuales`.
- Live grounded answering with
  `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cómo funciona la financiación de pólizas individuales en movilidad?' --product movilidad --document-type policy --top-k 5`
  now succeeds with `confidence=high` and lists `13.11. Financiación de
  Pólizas Individuales` as the leading documentary-basis item.
