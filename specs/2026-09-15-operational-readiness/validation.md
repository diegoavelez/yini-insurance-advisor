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

## Isolation Bundle Receipt — 2026-10-06

Work unit `YINI-READINESS-ISOLATION-IMPL-2`; role executor;
dispatch_owner `019f71d6-632c-7870-bfa2-89513fdeb85a`.
Terminal: `STOP_UNSAFE_VALIDATOR_INPUT`, not ready for independent review.
The three ordered checkout observations matched the required principal and
absolute `.git` common-dir. Source, allowlist, executable, symlink, runtime and
cache metadata matched the owner-bound binding; cache contents were not read.
The selected v3 observer ran once, exit 0, `MATCH`, exact fingerprint,
22 complete observations, and `successor_authority=false`.

Evidence directory: `/private/tmp/yini-isolation-impl2.AQcqJD`.
Observer result: `/private/tmp/yini-contract-ready.oo9hEX/observer-result.json`,
SHA-256 `cd1f1e08b80e13b9ff75be3342eaf0e12b9163c24aa46f72772175b78dce118f`.
The contract and preparation artifacts were verified against the renewal's
external hashes without reconstruction or rebinding.

Both focused invocations used the existing absolute
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.venv/bin/python`
with `-B -m pytest -p no:cacheprovider --basetemp <evidence-dir>/<phase>-tmp
tests/test_test_isolation.py -q`. Environment was constructed with `env -i`,
`PATH=/usr/bin:/bin`, `PYTHONPATH=.`, HOME/TMPDIR in the evidence directory,
`PYTHONDONTWRITEBYTECODE=1`, and `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`.

- RED: `red.log`, exit 1, one regression failed as intended. Its child exited
  2 during collection because inherited invented `TOP_K=18` overrode default 5.
  The child cwd contained only the invented dotenv/probe inputs relevant to
  Settings; no actual repository `.env` was read.
- GREEN: `green.log`, exit 0, one regression passed. The fresh child loaded the
  copied conftest before its module-level settings access, ignored invented
  dotenv and inherited credentials, retained cache identity and accepted an
  explicit test override to 7 during execution.
- Affected smoke checks and all four release groups: `NOT_RUN`. Inspection
  found `tests/test_retrieval.py:130-135` reads each supplied chunk file and
  extracts its text; `:281-294` invokes it using `expected_chunk_files` from
  the evaluation dataset. No synthetic replacement or authorized provenance
  is established for those filesystem inputs. The group was stopped before
  collection; the files and dataset were not opened to establish provenance.
- Production configuration and `tests/test_smoke.py` were not modified.
  No model, provider, network, private corpus, installation or Git write ran.
  No lint/type check or additional pytest phase ran after the terminal stop.

Read-only presentation truncations were paginated or reduced; an optional
`rg` lookup of nonexistent `docs/evaluation.md` exited 2, with the actual
`docs/evaluation-report.md` subsequently identified. This was an inspection
lookup issue, not an observer failure, RED cause or mutation. No observer retry
or fallback occurred. Renewed retry/adjustment, harness-repair and semantic
correction counters used: 0/2, 0/1, 0/2. Terminal stop invalidates remaining
balances. History and earlier documentary `NOT_RUN` entries remain intact.

Evidence ceiling: rung 2, one local deterministic isolation regression only.
Residual gaps include smoke/release validation, complete per-group safety,
lint, independent review and owner acceptance. Next owner decision: separately
scope synthetic filesystem inputs or another safe validation boundary, including
any necessary expansion beyond the current edit allowlist; do not skip tests,
read the corpus, or resume this terminal bundle automatically.

## IMPL-3 Corpus-Separation Receipt — 2026-10-06

Work unit `YINI-READINESS-ISOLATION-IMPL-3`; executor;
dispatch_owner `019f71d6-632c-7870-bfa2-89513fdeb85a`.
Terminal: `READY_FOR_INDEPENDENT_REVIEW`; no review or acceptance is claimed.
Physical repository is the principal
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor`, common-dir
its absolute `.git`. The three individual ordered bootstrap calls matched.
The externally checked predecessor manifest and both preparation sources
matched their owner hashes. Canonical successor is
`/private/tmp/yini-isolation-impl3-contract.json`, SHA-256
`10f1774f02b13a31574925ce3d565258e18c0a6de26d05233395b1bc78a550b0`.
V3 observer ran once: exit 0, MATCH, exact fingerprint, all 22 observations
complete, successor_authority=false. Fixed main HEAD
`b728c8e65a6bc575671ea7eb1e3c589f338bef17` was preserved.

### Local behavior and omissions

The two movilidad evaluations moved from eager dataset decorators to
`tests/test_corpus_evaluation.py`. The fixture loads all cases only during
explicit opt-in execution; both original loops/assertions are retained for
every case, including expected terms against actual chunk text. Zero cases
cannot pass. Cases now aggregate into two tests; counts are not comparable to
the old per-case parametrization and no real case count was collected here.
Two independent invented inline queries exercise filter normalization locally.
Backend unit tests use an explicit empty local corpus unless a test overrides
it with invented inline ChunkRecords; the real corpus assertion route is not
replaced by that fixture.

Additional references outside the edit allowlist were identified in
`tests/test_evaluation_dataset.py`: default loaders read questions,
golden-behaviors, retrieval-expectations, citation-expectations and acceptance
smokes under `data/eval`. The file remains byte-identical to HEAD. Default
collection ignores that entire file, including its synthetic contract tests;
its 36 functions are NOT_RUN here. Two default-dataset smoke tests remain
unchanged except their explicit corpus marker and are deselected locally.
These omissions are never local PASS or evidence of corpus quality.

`make test-release` now declares four local groups, with group 1 selecting
evaluation_runner, smoke and test_test_isolation. Groups 2–4 retain their source
lists. After a separate owner grant fixes dataset/chunk identities, provenance,
classification, allowed paths, access, safe runtime and operation bounds, the
distinct opt-in command is `make test-corpus-evaluation` (equivalently pytest
`--run-corpus-evaluation -m corpus_evaluation` on corpus_evaluation,
evaluation_dataset and smoke). This command was NOT_RUN; the option is an
explicit execution switch and does not itself grant authority or attest data.

### Observed validation

All pytest commands used the absolute existing `.venv/bin/python`, `-B`,
`-p no:cacheprovider`, temporary `--basetemp`, and a constructed environment:
PATH=/usr/bin:/bin, HOME/TMPDIR=/private/tmp, PYTHONPATH=.,
PYTHONDONTWRITEBYTECODE=1, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1. No inherited
credentials were copied. Final/correction commands used the external
`/private/tmp/yini-impl3-safe-pytest.py` wrapper with `-o addopts= -q`; it blocks
repository data/dotenv, actual model imports, network connection/resolution and
repository writes before pytest collection. Temporary fixtures are permitted.
The subprocess regressions install their own relevant boundaries or use only
invented inputs. This is bounded test evidence, not a universal OS sandbox.

| Phase | Exit | Actual result |
|---|---:|---|
| RED, new subprocess regression | 1 | Intended collection failure: FORBIDDEN_DATA_READ at the eager decorator, before actual read |
| GREEN, test_test_isolation.py | 0 | 2 passed |
| Final group 1 | 0 | 28 passed, 2 deselected, 0 boundary denials |
| Final group 2 | 0 | 15 passed, 0 boundary denials |
| Final group 3 | 0 | 93 passed, 0 boundary denials |
| Final group 4 | 90 | 262 passed, 21 failed; 21 chunk-directory enumeration attempts blocked before access |
| Correction 1, retrieval + test_test_isolation | 0 | 111 passed, 0 boundary denials |
| Focal ruff, five files | 1 | 8 preexisting E501 in retrieval |
| Focal ruff, other four files | 0 | All checks passed |

The first group-4 output was truncated by the tool; complete final counts and
all 21 failing test names were retained, while full tracebacks are unavailable.
No group was rerun to recover output. One semantic correction supplied the
missing empty-corpus unit fixture and extended the regression execution probe
to cover two formerly failing backend cases. Corrected coverage is 419 distinct
local cases by unchanged passes plus affected validation; no single clean
four-group final PASS is claimed. Corpus evaluation remains NOT_RUN.
Native HEAD retrieval lint baseline has 9 findings (the same 8 E501 plus I001);
the edited import block removes I001. No new lint issue was introduced.
No type checker was run (none is configured in pyproject).

Retry/pretarget-adjustment 0/2; harness repair 0/1; semantic correction 1/2.
Full local suite invocation 1/1; observer invocation 1/1. Final artifacts:
`/private/tmp/yini-impl3-receipt.md`,
`/private/tmp/yini-impl3-final-manifest.json`,
`/private/tmp/yini-impl3-candidate.diff`. The receipt binds complete command
lists, final path/hash/mode inventory and preservation observations.
Production core/config.py, raw index/config and foreign tasks/lessons.md are
preserved. No real dataset/chunk, actual dotenv/credential, model, provider,
network, installation, Git mutation or remote operation was executed.
Evidence ceiling: rung 2. Residual limitations: real evaluation, existing lint
debt, independent review and acceptance. This completed bundle grants no next
action; remaining balances cannot authorize another work unit.
