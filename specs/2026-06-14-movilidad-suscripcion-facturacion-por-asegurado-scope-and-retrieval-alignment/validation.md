# Validation

This slice is ready when suscripción `facturación por asegurado` queries are no
longer refused for unsupported scope and retrieve grounded evidence from the
correct suscripción family.

## Acceptance Checks

- The new spec bundle exists.
- Focused scope coverage proves the documented query pattern is supported.
- Focused retrieval coverage proves the `Facturación por asegurado` evidence chunk
  is preferred.
- At least one live `answer-query` run for the documented query returns
  `supported=true` with suscripción citations.

## Baseline Gap Evidence

- The live query
  `¿Qué condiciones aplican a la facturación por asegurado en pólizas colectivas?`
  currently returns an unsupported-scope refusal.
- Live retrieval for the same query can surface the suscripción family, but the
  exact chunk containing `Facturación por asegurado` conditions is not reliably
  selected first.

## Completion Evidence

- `./.venv/bin/python -m pytest tests/test_query_scope.py tests/test_retrieval.py -q -k 'asegurado or suscripcion or collective_billing'`
  passed after adding focused scope and retrieval regressions for the
  documented query pattern.
- `./.venv/bin/python -m ruff check core/query_scope.py rag/ingestion.py tests/test_query_scope.py tests/test_retrieval.py`
  passed.
- Live retrieval for
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué condiciones aplican a la facturación por asegurado en pólizas colectivas?' --product movilidad --document-type policy --top-k 5`
  now returns
  `movilidad__transversales__politicas-de-suscripcion-de-movilidad:v2:0109`
  first.
- Live grounded answering for
  `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué condiciones aplican a la facturación por asegurado en pólizas colectivas?' --product movilidad --document-type policy --top-k 5`
  now returns `supported=true`, `confidence=high`, and cites suscripción
  evidence instead of refusing for unsupported scope.
