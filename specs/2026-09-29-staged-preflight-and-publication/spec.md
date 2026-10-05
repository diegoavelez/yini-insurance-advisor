# Staged Preflight and Publication — Specification

## Status, depth and authority

Date: 2026-09-29. Work unit: `YINI-STAGED-PREFLIGHT-SPEC`.
Status: proposal for `READY_FOR_OWNER_SPEC_DECISION`, not an accepted spec or
`READY_FOR_IMPLEMENTATION`. SDD Level 2 is the smallest sufficient depth:
this changes a public observation schema and a cross-phase publication
contract. It adds no provider, service, deployment or production behavior.

Role: specification executor. Dispatch owner:
`019f71d6-632c-7870-bfa2-89513fdeb85a`. Route: `gpt-6-astra / high`.
Required physical repository:
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor`;
absolute common-dir: that root plus `/.git`. Principal checkout required,
no corrective cd, worktree selection, subagents or redelegation.

Current authority creates only the five Markdown files in this directory.
It permits the single bound v1 preflight and documentary integrity/postflight
checks. Implementation, product tests, formal review, acceptance, Git writes,
provider/network operations, publication, configuration and memory edits are
excluded. [validation.md](validation.md) binds the preserved initial state.

## Problem and intended outcome

The existing [v1 requirements](../2026-09-17-deterministic-readonly-preflight/requirements.md)
require `staged=[]` and permit only ` M` and `??` worktree rows. The current
script enforces that requirement. Thus a fresh commit task with valid staged
bytes cannot use v1 successfully. This is a coverage boundary, not a reason
to weaken v1 or reinterpret a failed invocation.

The dispatch also reports an ad hoc harness assuming porcelain record order
and inventing a full commit hash from a short prefix. These are supplied
incident context, not independently reconstructed findings. The proposed
contract compares maps and obtains full object IDs directly from Git.

For runtime permissions, the dispatch reports that auto-review rejected an
initial commit because the relayed authority was not trusted, while a later
explicit relay with normal escalation allowed commit/push. This is not proof
that delegation universally loses authority, nor that a repeated human
confirmation is always required. Repository/plugin policy and effective tool
permissions are different controls; neither guarantees approval by the other.

Outcome: owner-bound deterministic observation of ordinary empty or nonempty
staging, including partial staging, followed only by individually authorized
publication actions. Master prepares the exact task; executors verify the
received fixed point and return evidence without choosing successors.

## Proposed design decisions

1. Preserve v1 code, tests, schemas and failure semantics. Add the separate
   `scripts/staged_readonly_preflight.py` entry point for
   `yini-readonly-preflight/contract-v2` and `result-v2`.
   It rejects v1 input; v1 continues rejecting staged state.
2. Bind raw index SHA-256, canonical index tree identity, staged blob/mode/OID
   identities and raw worktree file identities separately. A partial file
   need not have identical staged and worktree bytes.
3. Support only principal, attached main, SHA-1 repositories with ordinary
   regular-file additions/modifications, including executable mode changes.
   Explicitly reject unsupported state; do not normalize it.
4. Keep the observer verify-only. Publication remains a documented process
   using separate grants; no new publication runner, scheduler or framework.
5. Select v1 or v2 from declared coverage before invocation and only after
   that mechanism's adoption. Missing coverage returns to the owner.
   There is no post-STOP fallback, ad hoc replacement or self-bound contract.

[requirements.md](requirements.md) owns exact inputs, outputs and invariants;
[plan.md](plan.md) owns fixed process sequences and future adoption;
[tasks.md](tasks.md) owns the bounded task graph; [validation.md](validation.md)
owns the acceptance matrix and separates current evidence from future tests.

## Security, limits and non-goals

No credentials, corpus, customer data or secret content enters fixtures,
contracts, logs or receipts. The caller binds only invented, public or
explicitly authorized files. The observer never dumps blobs, config values,
raw child output or environment values. Hashes do not sanitize unauthorized
data collection: uncertain data classification stops before content reads.

V2 excludes deletes, renames/copies, symlinks/hardlinks, submodules, merge
conflicts, intent-to-add, sparse/split indexes, assume-unchanged entries,
partial clones, alternates, relevant ignored/generated inputs, custom filters,
worktrees and other branches. A later requirement for any exclusion needs a
new owner decision and versioned scope, not a permissive switch.

Three physical scans and two Git observations detect visible races, not an
atomic snapshot. ABA changes, malicious concurrent writers, compromised
executables and tool bypass remain outside assurance. Exclusive checkout use
and trusted bound runtime/script identities are prerequisites. MATCH verifies
a bounded local observation; it does not authenticate or consume a grant,
enforce permissions, accept bytes, prove remote truth or authorize a successor.

No Full Access change, sandbox/approval bypass, plugin patch, new skill,
benchmark, ledger, dependency or global installation is proposed.

## Human decision and completion

The proposal fixes conservative defaults instead of reopening the interview.
Owner disposition remains necessary for accepting these exact bytes, choosing
the proposed I1 local objective bundle and its budgets, and authorizing later
independent review, adoption, acceptance and Git phases. Those are ungranted
lifecycle choices, not implementation assumptions.

No unresolved technical choice is delegated silently to the implementer.
If owner review changes supported states, the input/output contract, process
bounds or adoption scope, revise the spec before I1. Specification completion
requires all five documents, traced acceptance criteria, verified documentary
scope and preserved state. This task stops at `READY_FOR_OWNER_SPEC_DECISION`.

The live [execution state](../../docs/operations/execution-state.md) and
[roadmap](../roadmap.md) still project operational-readiness work. This proposal
does not update or override them. Canonical adoption is a later exact action
under the [executor workflow](../../docs/agents/executor-workflow.md),
[master-control topology](../../docs/operations/master-control.md) and
[ADR 0001](../../docs/adr/0001-read-only-master-control-topology.md).

## WorktreeConfig amendment candidate — 2026-09-30

Work unit: `YINI-WORKTREECONFIG-SPEC-AMENDMENT-RECOVERY-1`.
Status: `READY_FOR_OWNER_SPEC_DECISION` candidate, not accepted, implemented
or adopted. This appendix proposes v3 only; the preceding S1/v2 contract and
C1/O1 history retain their meaning. Dispatch owner and principal checkout
remain those stated above. Authority covers only these five specification
files and focal documentary checks.

The supplied diagnosis found that R3's unconditional `extensions.*` rejection
matches the accepted v2 implementation. It is a coverage limitation, not a
code defect against that spec. The dispatch reports local
`extensions.worktreeConfig=true`, repository format 0 and an absent principal
`.git/config.worktree`. This task verifies configuration byte identities and
principal absence without emitting or inspecting configuration values.
The configuration's author/origin is unproven; no attribution to Codex is made.
Disabling the extension can change configuration loading in linked worktrees
and is neither the proposed solution nor an authorized action.

The minimum proposed coverage is principal-only with explicitly bound
**absence** of `.git/config.worktree`, whether the extension is absent, false
or true. Every present principal config.worktree remains unsupported, including
a regular empty file; there is no unbound or implicitly ignored present file.
Supporting its contents/identity later requires another versioned decision.
Linked checkouts and their configuration files remain outside observation;
existing linked administrative directories do not themselves select a linked
checkout. Includes, every other extension, unsafe files and all other v2
exclusions remain rejected.

Use a distinct closed `contract-v3`/`result-v3` branch in the existing staged
observer's public verify/main seams, selected from the supplied schema before
any subprocess. V1 files remain untouched. V2 retains its exact schema,
result, sequence, extension rejection and accepted C1 behavior; no old contract
is silently upgraded, reinterpreted or tried again as v3. This avoids a second
copied observer while making the changed assurance explicit. Implementation
must retain a separately tested legacy v2 path, without a shared-framework
refactor.

[W1–W4](requirements.md#w1--candidate-contract-v3-and-compatibility) define
the proposed boundary; the [v3 process plan](plan.md#v3-candidate-process-plan)
orders configuration guards before configuration-dependent Git observations.
The [W01–W10 matrix](validation.md#worktreeconfig-public-seam-matrix--not_run)
is future evidence. Implementation, independent review, acceptance, adoption
and publication remain separate owner decisions. O1's candidate is not
accepted or replaced by this appendix.

## F3 prospective O1 projection clarification — 2026-10-02

The preceding WorktreeConfig appendix's pending O1 statement is historical.
For the current projection, dispatch transmits O1 owner acceptance after
independent FULL PASS through audit `01a0f475-4599-7aa0-ad68-83b0286d722f`,
final item `msg_03cd4fae84e8eb02016abd8ff1bd3087d19738ea1521fbf6eb`, native
review postflight `exec-b1ed1961-f902-4224-908a-e494f71ad020`, exit 0.
The full review thread ID is unavailable. No review is performed by this
appendix; [execution state](../../docs/operations/execution-state.md) owns
the received current projection.

S1/I1/C1/W-S1 receipts remain frozen. C1/O1 acceptance does not accept v3,
execute W01–W10, authorize publication or establish provider readiness.
The owner selected keeping LF after `Prior C1 and O1 acceptances remain
unchanged; neither accepts v3.` before `Git,` in [tasks.md](tasks.md).
The protected SHA-256 remains
`c0db211aea31ccaadc9d5e4c5049460eabddc2333a0a254859514c7230edbc80`.
This is a new byte disposition, not historical oracle PASS or renewed grant.
F3 remains a preparation candidate pending fresh application, independent
review and owner acceptance; F4 and global roadmap closure remain pending.
