# Executor and Checkout Boundary — Requirements

The original AC1–AC8 and sections below are preserved historical requirements
of the earlier correction. They do not authorize S1 or renew any earlier grant.
The **S1 prospective requirements** supplement at the end owns the new spec
candidate requirements; [spec.md](spec.md) states its documentary-only status.

Prospective amendment, 2026-09-17: S1-AC06 below is revised for the current
seven-document correction; the original phrase was "pages of at most 100
lines". Other historical grants and checks retain their original scope. The
dated [plan amendment](plan.md#capture-size-amendment--2026-09-17) separates
presentation targets from hard total budgets and owns the concrete recipe.

## Historical Correction Contract

## Objective and Authority

This bounded documentary correction implements the owner's accepted role,
dispatch, checkout, and recoverable-reading clarification. It is not product
work, independent review, acceptance, or operational-readiness continuation.
The current executor works in its received task; master control alone may
dispatch a later task under its separately named owner grant.

## Scope

Edit only repository-owned text in `AGENTS.md` outside its managed marker,
`docs/agents/executor-workflow.md`, `docs/operations/master-control.md`, one
brief lesson in `tasks/lessons.md`, and this directory's `requirements.md`,
`plan.md`, and `validation.md`. This owner-bounded minimal spec does not
expand the allowlist or copy the installed Operating Model.

## Acceptance Criteria

- AC1: Master control is the sole administrative dispatcher under an exact
  owner grant. An executor performs the received task, never creates, forks,
  hands off, or sends another task, and never reselects its checkout. Reading
  master-control instructions does not change the executor's role. A fresh
  task means this isolated received task, not recursive redelegation.
- AC2: Yini defaults to its principal checkout. A worktree requires explicit
  owner selection and a reason. An unmet isolation need is returned to the
  owner; it never authorizes worktree creation or corrective `cd`.
- AC3: Before other repository work, preflight observes `pwd -P`, Git root,
  and common-dir using read-only Git with `GIT_OPTIONAL_LOCKS=0`. Relative
  common-dir output is resolved against the observed physical directory.
  A checkout mismatch stops without changing directories or checkouts.
- AC4: Handoffs and terminal receipts declare role, `dispatch_owner`, physical
  repository, absolute common-dir, and the checkout precondition. Existing
  fixed-point, allowlist, action, gate, and evidence requirements remain.
- AC5: Incomplete or truncated read-only output is recovered by bounded
  pagination through EOF. It is continued capture, not a mutating retry or
  renewed grant. No mutation is repeated; real drift, write failure,
  unexpected non-capture tool failure, secrets, or scope conflict still stop.
- AC6: State explicitly that these are contractual controls. No per-task
  tool-allowlist schema or hard enforcement has been demonstrated, and no
  tool removal or runtime/configuration change is claimed.
- AC7: Preserve the five owner-declared readiness deltas byte-for-byte with
  mode `644`, empty staged delta, original HEAD/branch/index, and the managed
  marker. Limit new deltas to the seven allowed paths.
- AC8: Report historical calls separately from inference and unobserved
  outcomes. Worktree inventory does not establish a clientThreadId mapping.
  The later delegation test remains pending with master control.

## Exclusions and Evidence Ceiling

No subagents, dispatch, worktree creation/removal/pruning, cleanup, Git
mutation, plugin/config/cache/marketplace changes, network, providers,
secrets, corpus, application imports, pytest, new software test harness, or
R1H1 `advise` invocation. Only documentary checks are authorized. Static
evidence is at most rung 1 and cannot guarantee future executor behavior.

## S1 Prospective Requirements — 2026-09-16

These are testable requirements for the proposed future recipe and control
flow, not claims that it has been implemented or executed. S1 verifies their
documentary presence and consistency only. [plan.md](plan.md) is the sole
owner of the literal recipe and transition graph; [validation.md](validation.md)
maps future scenarios separately from S1 checks.

| ID | Acceptance criterion |
|---|---|
| S1-AC01 | The closed recipe names every permitted inspection invocation, order, explicit inputs, expected result, and exit semantics; no improvised command, hidden command chain, or mutation is an inspection step. |
| S1-AC02 | Initial physical cwd is observed without a cwd/workdir override, login shell, or corrective `cd`; Git root and absolute common-dir must match the grant before other repository work. |
| S1-AC03 | The fingerprint binds physical identity, branch/HEAD, raw index SHA-256, staged delta, exact tracked/untracked manifest with kind/mode/hash, managed marker, and registered worktrees; governed/allowed ignored/forbidden/derived partitions are explicit. |
| S1-AC04 | A raw index digest is never replaced by a tree OID. `git write-tree`, `git read-tree`, `git update-index`, and `git hash-object -w` are prohibited strings to inspect, never commands to execute for verification. Missing index bytes stop without creating an index. |
| S1-AC05 | Owner-permitted foreign entries are compared against their exact manifest and preserved; any unexpected path, status, mode, or hash stops. A dirty but fully inventoried candidate need not be cleaned. Counts are derived from the manifest, not hardcoded to a reusable 6M/8?? total. |
| S1-AC06 | One authorized source per capture; 100 lines is an initial pagination target, not an acceptance/safety invariant or universal input limit. Configurable character/token presentation controls split retained output before emission, including long lines; source/range/exit and completeness are retained separately. Complete oversize with expected exit is not a size failure; incomplete output remains INCOMPLETE until bounded recovery. `read_thread` uses one turn and 6500 characters per included output, which does not prove completeness. Explicit total call/page budgets remain hard. |
| S1-AC07 | Optional absence, expected no-match, and incomplete capture have bounded read-only continuations in the same task. Their symptom, classification, continuation, and remaining gap are recorded; no missing content or PASS is inferred. Required absence after safe lookup is a real block. |
| S1-AC08 | Envelope type, `isError`, protected parsing, record shape, and nested truncation are checked through the existing C1 helper pointer before structured traversal. Tool errors and invalid shapes are not valid records; only authorized native output/records may support a fallback. |
| S1-AC09 | True drift, unknown mutation, write failure, sensitive-data risk, exhausted bound, unsafe/unexpected non-capture failure, truth conflict, or material ambiguity terminates work. Read-only recovery never repeats a mutation, escalates permissions, changes refs, or renews a grant. |
| S1-AC10 | Mermaid and transition table have the same guards, actors, inputs, outputs, and terminal behavior. Each lifecycle task has its own grant and fresh physical/fingerprint preflight. Edges express eligibility only, never authority. |
| S1-AC11 | FULL is required initially and after a new trust boundary, public contract, or transversal topology. NARROW_DELTA requires a prior applicable FULL and explicit qualification. Review remains independent, read-only, candidate-bound, and separately authorized. |
| S1-AC12 | At most two semantic finding/correction/review cycles follow FULL. C1/C2 require exact preauthorization and new visible tasks plus fresh review; exhaustion returns to the owner. Severity and acceptance conflict remain governed by the installed validation contract. |
| S1-AC13 | Future delivery updates the relevant canonical workflow and lessons before review, under its own allowlist. Checks or reviews cannot cure an earlier preflight mismatch. S1 does not edit those canonicals or claim delivery. |
| S1-AC14 | PASS ends at READY_FOR_OWNER_DECISION; owner acceptance, Git, readiness, provider, and external actions retain separate named authority. Git/provider nodes visibly stay blocked without it and contain no mutating command recipe. |
| S1-AC15 | Historical R1 STOP, H1, R2 findings, C1 evidence, the workdir caveat, R3 failure, and G1 failure keep their original evidence limits. S1 checks are static only; future runtime/rendering checks remain NOT_RUN. No hard-enforcement or savings claim is made. |
| S1-AC16 | S1 touches only the five named spec paths; nine protected deltas, index, marker, branch/HEAD, and worktrees are preserved. Its capsule reports exact changes, staged delta, fourteen final hashes/modes, checks/skips, role/dispatch owner, evidence ceiling, and READY_FOR_OWNER_SPEC_DECISION. |

### Current S1 Authority and Preserved State

Role `executor`; dispatch owner `019f71d6-632c-7870-bfa2-89513fdeb85a`;
principal checkout only; Astra/high for the transversal contract. The initial
manifest has twelve deltas, all regular mode `644`, and empty staged state.
Adding only `spec.md` and `tasks.md` yields fourteen deltas: six tracked modified
files and eight untracked spec files. These are S1 expectations, not a generic
recipe constant. The grant's initial hashes are checked afresh and the final
candidate hashes belong in the terminal receipt, avoiding self-reference.

Protected byte-for-byte: `AGENTS.md`, `docs/agents/executor-workflow.md`,
`docs/operations/master-control.md`, `tasks/lessons.md`,
`docs/operations/execution-state.md`, `specs/roadmap.md`, and the three
`specs/2026-09-15-operational-readiness/{requirements,plan,validation}.md`
files. Ignored pre-existing state remains untouched and supplies no evidence.

The current owner's bounded exception permits safe read-only search/capture
recovery for producing S1. Future adoption of that broader lookup rule needs
operational materialization under a new grant. Existing workflows and all real
failure stops remain in force; no old grant or repair budget is revived.

## Capture Correction Acceptance Criteria — 2026-09-17

- CAP01: Revise S1-AC06, C3/V3, graph/table capture guards, and the workflow
  pointer coherently; keep the recipe body solely in `plan.md`.
- CAP02: Complete authorized output above 100 lines is not a size error.
  Oversize alone never supplies `HARNESS_DEFECT` to the advisory facade.
  Historical explicit hard-grant breaches and STOPs are not excused.
- CAP03: Truncation or missing ranges remain INCOMPLETE; recovery retains exact
  source/ranges and exit within the same task and hard total allowance. If a
  buffer is unavailable, only bound read-only re-observation with identity
  rechecks is eligible; never replay a mutation or hide an error with a pipe.
- CAP04: Real non-capture errors, drift, secrets/unsafe capture, unknown or
  failed mutation, and exhausted total budgets remain terminal. No escalation,
  renewed authority, or fabricated output is allowed.
- CAP05: Run ephemeral invented fixtures for 101 complete lines, one line
  above 6500 characters, truncated recovery, error exit, drift, exhausted
  budget, and mutation replay refusal. Verify concatenation and exit retention
  against the amended literal pagination body; semantic routing remains a
  manual table assessment, not new classification software.
- CAP06: Preserve the five readiness deltas; change only the seven allowed
  tracked files; derive pre/post hashes, inspect diffs, links and coherence,
  run scoped `git diff --check`, and retain HEAD/index/marker/staging. Return
  twelve final delta identities and the actual checks/skips and balances,
  without claiming review, acceptance, product behavior, or runtime enforcement.
