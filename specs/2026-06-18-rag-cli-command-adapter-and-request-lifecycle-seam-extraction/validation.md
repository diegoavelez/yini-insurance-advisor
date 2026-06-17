# Validation

This slice is ready when the CLI entrypoint keeps the same public behavior but
no longer mixes parser definitions, thin command adapters, and request
lifecycle orchestration in one large surface.

## Acceptance Checks

- `rag/cli_runtime.py` exists and owns the shared `RetrievalQuery` builder plus
  request lifecycle orchestration;
- `rag/ingestion.py` remains the façade that keeps parser definitions and the
  public `main(...)` entrypoint;
- focused tests cover shared query construction, request-id fallback, and
  request lifecycle success/failure logging;
- the roadmap records the slice as closed.

## Completion Evidence

- `./.venv/bin/python -m pytest tests/test_cli_runtime.py tests/test_observability.py tests/test_retrieval.py tests/test_grounded_answer_generation.py -q`
  passes;
- `./.venv/bin/python -m ruff check rag/cli_runtime.py rag/ingestion.py tests/test_cli_runtime.py --ignore E501`
  passes;
- `rag/ingestion.py` no longer duplicates `RetrievalQuery(...)` construction
  across retrieval and grounded-answer command runners;
- top-level CLI request lifecycle logging/dispatch now flows through the
  dedicated seam.
