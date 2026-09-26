# Plan — operational-readiness

## Objective

Prepare the Level 1 `YINI-OPERATIONAL-READINESS-001` candidate for documentary
review. The candidate maps the existing operational baseline to a bounded
evidence plan; it does not execute that plan.

## Affected Files

- `specs/2026-09-15-operational-readiness/requirements.md`
- `specs/2026-09-15-operational-readiness/plan.md`
- `specs/2026-09-15-operational-readiness/validation.md`
- `docs/operations/execution-state.md`
- `specs/roadmap.md`

## Assumptions and Boundaries

- `docs/mvp-go-live.md` is the existing operational baseline and remains the
  only linked go-live procedure for this slice.
- `make test-release` declares four sequential `pytest` invocations using
  `.venv/bin/pytest`; its static text is an inventory, not a passed gate.
- `pyproject.toml` is the dependency source of truth. Its declared provider
  packages do not prove that any package, credential, endpoint, model cache, or
  corpus is available in the current environment.
- The reviewed seams show configuration requirements for Qdrant and Groq,
  Qdrant-client construction, locally constrained embedding loading, and a
  separately named embedding warmup path. This does not establish a global
  execution-isolation guarantee.

## Risks

- A local green gate would still not demonstrate provider, hosted, human, or
  production readiness.
- The static test reading did not prove network/provider/corpus isolation, and
  it did not prove the converse. That evidence remains unavailable here.
- A benign application query can invoke provider-backed work and may incur
  charges; it cannot be scheduled until a separate owner fixes the applicable
  cost contract and spend ceiling.
- A public or synthetic question does not constrain retrieved evidence: the
  application prompt includes selected chunk text and metadata before Groq
  generation. A configured private corpus could therefore enter the provider
  payload even when the question itself is benign.

## External Protocol Proposal — Not Authorized

All three stages require a fresh visible provider-execution task, a current
configuration/contract preflight, sanitized evidence, human review where
specified, and no retries. No stage is authorized by this document.

| Stage | Exact maximum application operations | Permitted data | Proposed timeout | Proposed budget and stop |
|---|---:|---|---:|---|
| Qdrant availability and contract | 1 metadata read of the configured collection | no corpus payload; collection metadata only | 10 seconds | expected inference spend: 0 because this is metadata, not generation; request/billing terms are unknown. Stop before invocation unless the provider contract fixes the request-cost treatment; stop on any unknown cost or contract. |
| Hugging Face load/readiness | 1 public readiness/load observation | public model identifier and public endpoint state only; no private prompt or corpus | 30 seconds | expected inference spend: 0 because this is readiness/load observation, not generation; transfer/request billing is unknown. Stop before invocation unless the applicable cost/contract is fixed; stop on any unknown cost or contract. |
| Benign application query with human citation review | 1 application invocation | controlled synthetic evidence or an explicitly authorized public corpus, with an in-scope public or synthetic query; no personal, client, secret, or private-corpus data in the query, retrieved context, or complete provider payload | 30 seconds | potentially charged provider-backed inference. The inference spend ceiling is **BLOCKED — owner/provider amount not yet defined**; perform 0 operations until it is fixed. If later authorized, a human reviews the answer and citations; stop on any unknown cost, contract, timeout, or response/citation concern. |

Before stage 3 can be proposed for execution, a separate task must identify and
bound the selected evidence source, verify each source's identity, provenance,
classification, and permission for the specific provider/destination, and
demonstrate that retrieval is isolated to that source before any retrieval or
transmission. It must verify that the resulting query, every retrieved fragment
and metadata field, and the complete payload sent to the provider satisfy the
same exclusions before transmission. A generic authorization statement is not
evidence that private content is permitted. Do not fall back to the configured
corpus; if the selection, isolation, provenance, or payload check cannot be
demonstrated safely, stop with zero stage-3 operations. The corpus, provider
contract, and spend amount remain undecided here.

The cap counts application operations, not hidden provider calls. No keepalive,
permanent readiness, or recurring health guarantee is inferred from a successful
stage. A failure, timeout, unexpected response, changed contract, or any
unresolved cost terminates its stage without repair, retry, or escalation.

## Documentary Execution Steps

1. Record the local command/dependency inventory and evidence gaps.
2. Bind the proposal above to a later separately authorized external task.
3. Update semantic state and the roadmap without altering the phase-completion
   history or the existing go-live baseline.
4. Run only documentary integrity checks on the candidate and return it for
   independent review and owner disposition.
