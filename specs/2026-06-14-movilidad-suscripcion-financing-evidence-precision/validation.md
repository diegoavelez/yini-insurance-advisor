# Validation

This slice is ready when financing-individual suscripción answers keep `13.11`
first and stop surfacing unnecessary lateral policy sections ahead of direct
financing evidence.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval coverage proves direct financing sections outrank unrelated
  lateral suscripción sections for the documented financing query pattern.
- At least one live `retrieve-chunks` run for the documented financing query
  returns `13.11` first and no longer places `14.1` ahead of direct financing
  evidence.
- At least one live `answer-query` run for the documented financing query keeps
  a supported grounded answer while focusing documentary basis and citations on
  direct financing evidence.

## Baseline Gap Evidence

- Live retrieval with
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo funciona la financiación de pólizas individuales en movilidad?' --product movilidad --document-type policy --top-k 5`
  now returns `13.11` first, but still includes
  `14.1. Cotización de Pólizas Colectivas` ahead of additional direct financing
  evidence.
- Live grounded answering with
  `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cómo funciona la financiación de pólizas individuales en movilidad?' --product movilidad --document-type policy --top-k 5`
  succeeds, but the documentary basis still includes lateral collective-policy
  evidence that is not necessary for the financing answer itself.

## Completion Evidence

- Focused regression coverage passes with
  `./.venv/bin/python -m pytest tests/test_retrieval.py tests/test_grounded_answer_generation.py -q -k 'financing or collective_billing or renewal or normalize_query_skips_document_name or lateral_suscripcion_financing_evidence'`.
- Static verification passes with
  `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py tests/test_grounded_answer_generation.py`.
- Live retrieval with
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo funciona la financiación de pólizas individuales en movilidad?' --product movilidad --document-type policy --top-k 5`
  now returns `13.11. Financiación de Pólizas Individuales` first and
  `13.1. 2. Cambio de Plan de Pagos Anual Financiado` second, ahead of
  `14.1. Cotización de Pólizas Colectivas`.
- Live grounded answering with
  `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cómo funciona la financiación de pólizas individuales en movilidad?' --product movilidad --document-type policy --top-k 5`
  now succeeds with `confidence=high` and exposes only the direct financing
  sections `13.11` and `13.1.2` in documentary basis and citations.
