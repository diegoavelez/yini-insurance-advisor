# Validation

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.

## Required Checks

- `./.venv/bin/python -m rag.ingestion answer-query --query "cobertura del plan PAC 60 más" --top-k 3`

## Required Scenarios

- Retrieval succeeds against the indexed sample corpus.
- Groq completion succeeds with the validated model identifier.
- The final grounded answer includes citations and a supported verification
  outcome.

## Merge Readiness

This spec is ready when the validated Groq runtime configuration is explicitly
documented and the local answer path succeeds end-to-end.

## Evidence

- `./.venv/bin/python -m ruff check tests/test_observability.py`
- `./.venv/bin/python -m pytest tests/test_observability.py -q`
- `./.venv/bin/python -m rag.ingestion answer-query --query "cobertura del plan PAC 60 más" --top-k 3`

## Recorded Outcome

- The validated Groq model identifier is `openai/gpt-oss-120b`.
- Tracked configuration examples now match the validated runtime identifier.
- A real end-to-end `answer-query` run succeeded with:
  - retrieval from Qdrant;
  - completion from Groq;
  - grounded citations and `supported: true`.
