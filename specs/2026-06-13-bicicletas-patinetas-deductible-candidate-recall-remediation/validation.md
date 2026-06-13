# Validation

- Local lexical recall prefers explicit `DEDUCIBLE` chunks for deductible-intent
  mobility queries.
- Existing retrieval regressions continue to pass.
- The real deductible query now cites stronger deductible evidence.

## Suggested Checks

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
- `./.venv/bin/python -m ruff check tests/test_retrieval.py rag/ingestion.py`
- `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es el deducible del seguro de bicicletas y patinetas?' --product movilidad --top-k 5`
