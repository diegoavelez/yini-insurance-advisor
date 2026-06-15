# Validation

This slice is ready when grounded-answer assembly and guardrail helpers live
behind their own `rag` seam and the validated response behavior remains
unchanged.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_grounded_answer_generation.py tests/test_observability.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/grounded_answers.py tests/test_grounded_answer_generation.py tests/test_observability.py`
3. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`

## Expected Evidence

- prompt/citation/documentary-basis helpers still behave deterministically;
- insufficient-evidence and refusal outcomes still match the current typed
  contracts;
- correlated grounded-answer observability still passes;
- a live grounded-answer query still succeeds against the existing runtime.
