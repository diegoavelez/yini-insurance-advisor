# Validation

This slice is ready when VIAJES coverage smokes still resolve to the correct clausulado family and now surface `SECCIÓN I QUÉ CUBRE ESTE SEGURO` evidence.

## Acceptance Checks

- A committed spec bundle exists for `viajes-coverage-section-priority-recovery`.
- VIAJES coverage queries append focused coverage recall terms.
- Live national retrieval includes `SECCIÓN I QUÉ CUBRE ESTE SEGURO` in the top results.
- Live international grounded answering cites `SECCIÓN I QUÉ CUBRE ESTE SEGURO` evidence.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'viajes_coverage_query'`
- `./.venv/bin/python -m ruff check tests/test_retrieval.py --ignore E501`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el seguro de viaje nacional?' --product viajes --document-type policy --top-k 5`
- `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre el seguro de viaje internacional?' --product viajes --document-type policy --top-k 5`
