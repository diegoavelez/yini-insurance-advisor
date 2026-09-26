# Validation — operational-readiness

## Evidence Status

This work unit permits documentary inspection only. The status labels below
describe what was observed in this candidate; they do not report product,
provider, hosted, release, deployment, pilot, production, or acceptance
evidence.

| Check or group | Static inventory | Execution status | Limit |
|---|---|---|---|
| `make test-release` | `Makefile` declares four sequential `PYTHONPATH=. .venv/bin/pytest ... -q` commands | `NOT_RUN` | No `make` or `pytest` authority was granted. |
| Evaluation and smoke | `tests/test_evaluation_dataset.py`, `tests/test_evaluation_runner.py`, `tests/test_smoke.py` | `NOT_RUN` | No result is available for this work unit. |
| MCP compatibility | `tests/test_mcp_server.py`, `tests/test_mcp_client.py`, `tests/test_mcp_compatibility.py`, `tests/test_mcp_versioning.py` | `NOT_RUN` | No result is available for this work unit. |
| UI, workflow, scope, guardrails, observability | `tests/test_app_ui.py`, `tests/test_observability.py`, `tests/test_query_scope.py`, `tests/test_guardrail_abuse_cases.py`, `tests/test_langgraph_workflow.py` | `NOT_RUN` | No result is available for this work unit. |
| Retrieval and ingestion seams | `tests/test_retrieval.py`, `tests/test_grounded_answer_generation.py`, `tests/test_document_canonicalization.py`, `tests/test_term_equivalences.py`, `tests/test_embedding_generation.py`, `tests/test_qdrant_indexing.py`, `tests/test_cli_runtime.py`, `tests/test_ingestion.py` | `NOT_RUN` | No result is available for this work unit. |

## Declared Dependency and Side-Effect Inventory

- The local gate resolves its executable through `PYTEST ?= .venv/bin/pytest`.
- `pyproject.toml` declares `pytest` for development and runtime packages that
  include `qdrant-client`, `sentence-transformers`, and `groq`.
- `core/config.py` requires Qdrant configuration when that feature is enabled;
  `rag/qdrant_store.py` constructs the configured client; and
  `rag/runtime_providers.py` creates the Groq client only through its runtime
  path.
- `rag/runtime_providers.py` and `rag/pdf_conversion.py` show the reviewed
  local-only embedding-load mechanism; `rag/ingestion.py` separately documents
  a warmup path that permits a networked model load.

These are static references only. The inspected test files use local fakes and
monkeypatching in individual cases, but this work did not execute or exhaustively
analyze the suite. Therefore network, provider, and corpus isolation are
**NOT DEMONSTRATED**. This is an evidence gap, not a product failure and not a
claim that any test makes a network call.

## Documentary Checks for This Candidate

- C1 documentary correction, `2026-09-26`: the initial read of all five
  candidate paths completed. UTF-8 decoding, final newline, trailing-whitespace
  and conflict-marker checks passed on all five. No Markdown relative links
  occurred in these files; the referenced `docs/mvp-go-live.md` exists. The
  candidate's edit allowlist is only this directory's `plan.md` and
  `validation.md`; the other eight preflight delta paths are protected.
- C1 pre-recording whitespace checks, `2026-09-26`: tracked `git diff --check`
  exited 0 with no diagnostics. Each of the five untracked files was checked
  with `git diff --no-index --check /dev/null <path>`; each exited 1 for the
  expected file difference with no whitespace diagnostics. Final readback and
  fixed-point postflight after this record belong to the C1 receipt.
- The earlier independent `FULL` review (task
  `01a0def4-228d-7642-aad7-e9d48ef1a32c`) found P2: the stage-3 proposal
  constrained the public/synthetic question but did not establish that
  retrieved private corpus text would be excluded from the Groq prompt.
  Static review of `rag/ingestion.py` and `rag/grounded_answers.py` confirms
  selected retrieved chunks are included in the completion prompt. The C1
  `plan.md` correction adds an evidence-source and full-payload precondition;
  it has not received independent differential review or owner acceptance.
- product tests, application-importing validators, `make`, `pytest`, provider
  calls, corpus access, and Git mutation: `NOT_RUN` by authority boundary.
  Differential review of the C1 candidate is `PENDING`, not a PASS.

## Evidence Ceiling

At most rung 1, static/documentary evidence. The C1 pre-recording checks above
passed; final readback and fixed-point postflight are reported in its receipt.
A candidate ready for documentary review is not operational
readiness and does not authorize a later check.
