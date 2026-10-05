# Executor Workflow

## Purpose

Executor tasks perform one bounded lifecycle action under an explicit owner
grant. They do not act as master control, choose the next strategic unit,
self-review formally, self-accept, or inherit successor authority.

## Visible Task Topology

Each executor objective and later independent review or lifecycle phase uses a
fresh visible Codex task. Only an owner-selected opt-in local objective bundle
may include scoped implementation, affected validation, and finite correction
in that same executor task, under the installed plugin's
`references/authority-grants.md` contract. A previously issued action-specific
grant keeps its literal fresh-task rule. Git actions, publication, provider
execution, deployment, pilot, production, and external actions remain separate
authorities. Task and worktree selection create no authority.

Master control is the sole administrative dispatcher under an exact owner
grant. An executor performs the task it received; it never creates, forks,
hands off, or sends another task, or reselects its checkout. Reading
`docs/operations/master-control.md` does not change that role. Here, a fresh
visible task means the isolated task already received, not an instruction to
redelegate. Return a needed successor or isolation decision to master/owner.

## Checkout Boundary

Yini's default is the principal checkout at
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor`.
A worktree requires explicit owner selection and a stated reason before
dispatch. If safe execution needs isolation absent that grant, return the
need; do not create, remove, prune, or select a worktree yourself.

Before any other repository work, observe `pwd -P` and the Git root/common-dir
with `GIT_OPTIONAL_LOCKS=0`. Resolve relative common-dir output against the
observed physical directory and compare physical identities with the handoff.
A mismatch stops without corrective `cd`, task creation, or checkout changes.
For a fresh grant after review and owner acceptance of the applicable O1
adoption, use the coverage-selected deterministic observer below
to verify the granted branch/HEAD, index, inventory, bytes, and modes.
Explicitly inventoried owner-permitted foreign changes remain untouched and
do not require a clean working tree; any undeclared delta still stops.

These rules are contractual controls, not hard enforcement. No per-task
tool-allowlist schema has been demonstrated for this boundary. Do not claim
tools were removed or change Codex, plugin, cache, or marketplace configuration
to implement this documentary rule.

## Deterministic Preflight and Bounded Recovery

For fresh grants after independent documentary review and owner acceptance
of `YINI-STAGED-PREFLIGHT-O1`, use the named
[bootstrap](../../specs/2026-09-17-deterministic-readonly-preflight/plan.md#bootstrap-and-later-adoption)
as three individual, ordered calls before any other Git observation. Then
select the mechanism from the grant's declared coverage before invocation:

- v1 `scripts/readonly_preflight.py` for eligible empty staging (`staged=[]`)
  and only ` M`/`??` worktree rows under its unchanged
  [R2 contract](../../specs/2026-09-17-deterministic-readonly-preflight/requirements.md#r2--exact-input-schema)
  and [R6 result](../../specs/2026-09-17-deterministic-readonly-preflight/requirements.md#r6--exact-deterministic-result);
- v2 `scripts/staged_readonly_preflight.py` for compatible `empty_staged` or
  `staged_regular` state under the closed
  [v2 coverage and contract](../../specs/2026-09-29-staged-preflight-and-publication/requirements.md#r2--closed-contract-v2-schema)
  and [result-v2](../../specs/2026-09-29-staged-preflight-and-publication/requirements.md#r4--closed-result-v2).
  Under the accepted v1/v2 selection, nonempty ordinary regular-file staging
  requires v2; partial staged/worktree bytes and mode-only changes retain
  their separately bound identities. A later accepted v3 selection applies
  only to its explicitly bound v3 coverage.

### Prospective v3 Coverage-Selection Adoption Candidate (2026-10-03)

Candidate for `YINI-W3-ADOPTION-1`; inactive pending its own independent
documentary review and owner acceptance of these exact bytes. Until both gates
pass, the accepted v1/v2 selection above remains in force and v3 is not a
procedural choice. This candidate records received W-I1 implementation
acceptance after W-R1 `FULL_PASS`; it does not repeat either decision or accept
the adoption candidate itself.

After adoption, select v3 only when the owner-bound grant explicitly requires
the proposed principal, absent-only `config.worktree` coverage and supplies a
closed
[`contract-v3`](../../specs/2026-09-29-staged-preflight-and-publication/requirements.md#w1--candidate-contract-v3-and-compatibility)
contract binding repository format 0, `extension_worktree_config` as null,
true or false, and `config_worktree: {"state":"absent"}`. The checkout must
be the attached principal `main` checkout. Every other v2 constraint and
exclusion remains in force; `.git/config.worktree` must be absent, and any
present leaf, linked-checkout configuration, other extension, include, or
unsupported state remains unsupported. V2 continues to reject
`extensions.worktreeConfig`; v1 retains its empty-staged coverage and exact
meaning. The grant's declared coverage selects v1, v2 or v3 before invocation;
there is no schema/version probing, post-STOP switch, fallback, retry or
rebound contract. Missing or unsupported coverage returns to the owner.

V3 selection does not change the separate publication transitions in the
[staged-preflight plan](../../specs/2026-09-29-staged-preflight-and-publication/plan.md#proposed-publication-transitions)
or grant implementation, review, acceptance, staging, commit, push, remote
readback or provider authority. MATCH remains bounded local observation only.

Invoke the selected trusted observer once, using verified absolute Python
`-B`, script and Git identities, exact owner-bound contract bytes on stdin and
their externally bound SHA-256. Remove inherited `GIT_*` names except
`GIT_OPTIONAL_LOCKS=0` without printing values. Check process exit and the
complete version-specific result, exact fingerprint and
`successor_authority=false` together. `STOP`, nonzero exit, incomplete or invalid output, unsupported
coverage, or mismatch ends the task without retry, repair or ad hoc Git
substitution. `MATCH` establishes only the bounded local observation; the
named task action still needs its separate authority and matching fixed point.
Selection is never version probing: missing coverage or an unavailable
mechanism stops before invocation, and a failed invocation has no alternate
observer, ad hoc substitute or rebound expectation. Mandatory use begins only
after O1 review and owner acceptance; this candidate does not self-accept,
change v1 meaning or renew an earlier grant.

Publication follows the separately granted
[R5–R6 contract](../../specs/2026-09-29-staged-preflight-and-publication/requirements.md#r5--publication-authority-and-expected-transitions)
and [P0–P7 transitions](../../specs/2026-09-29-staged-preflight-and-publication/plan.md#proposed-publication-transitions):
preflight (P0), authorized stage if needed (P1), expressly authorized
successor capture (P2), verify-index (P3) with the single version selected by
the accepted coverage rule at P0, commit (P4), native full OID and
parent/tree/path verification (P5), then push (P6) under its own grant and
receipt (P7). For the accepted v1/v2 selection, P3 uses only the selected
v1 or v2 contract and its complete version-specific result; the prospective
v3 clause governs P0/P3 only after its own review and owner acceptance. Never
require a second observer version for the same P0/P3 transition. The installed
authority contract owns grant forms; these pointers add no publication runner
or authority. Normal named
permission escalation remains subject to runtime review; denial ends the
attempt without automatic retry. Push is transport evidence only and triggers
no automatic canonical-document reconciliation.

The accepted executor-and-checkout-boundary specification is historical. Its
[`plan.md`](../../specs/2026-09-15-executor-checkout-boundary/plan.md) retains
the earlier textual recipe, transition graph and read-only capture guidance;
it is not an alternate branch/index/status preflight after O1 acceptance.
Fresh grants still bind complete inputs, sources, bounds and selected checks.

Historically, a delivery task using that plan updated the applicable canonical
workflow and any narrowly evidenced lesson within its own allowlist. A later
check or PASS cannot cure a failed physical preflight, fingerprint mismatch,
or exhausted total read-call/page budget. True drift, unknown mutation, write failure,
sensitive-data risk, unsafe non-capture failure, truth conflict, or material
ambiguity remains a terminal stop and needs owner disposition; neither this
pointer nor capture recovery authorizes a retry, repair, escalation, cleanup,
or successor action.

## Internal Subagents

An internal subagent is support, not a visible task. It may be used only for at
least two independent, bounded, non-mutating analysis workstreams when focused
coverage or wall time justifies it. It never substitutes for a lifecycle task,
retry, implementation, correction, review, Git action, or external action.

## Handoff Contract

Every executor handoff must state:

- role and `dispatch_owner` (the master task realizing the named owner grant);
- checkout precondition: principal or explicit owner-selected worktree with
  reason, required physical repository and absolute common-dir, and a stop
  on mismatch before any corrective directory or checkout selection;
- objective and explicit non-goals;
- physical repository, Git common-dir, exact fixed point, and initial inventory;
- active requirements and validation sources;
- exact path allowlist and governed read-only inputs;
- assumptions and known unknowns;
- acceptance criteria and verification commands;
- separately named permitted authorities and explicitly excluded actions;
- required model/reasoning route or validated deterministic mechanism;
- fail-closed conditions and required return evidence.

If the requested work cannot stay inside this contract, stop and return the
scope conflict instead of widening the task.

## Reasoning-Necessity Dispatch

- No new semantic decision: use a validated deterministic mechanism and no
  model when one exists.
- Semantic validation only: deterministic execution first, then a bounded LLM
  or human semantic validator in the applicable task.
- New bounded or open decision: use the manual route below or return the
  decision to the owner.

Failed guards, invalid output, drift, unavailable mechanisms, and ambiguity
stop fail-closed.

## Manual Yini Routing

| Work classification | Required route |
|---|---|
| validated deterministic mechanics | validated mechanism, with no model when one exists |
| ordinary Master Control | `gpt-6-astra / medium` |
| architecture, transversal decisions, material contradictions, or high-risk migrations | `gpt-6-astra / high` |
| bounded implementation, tests, refactors, or ordinary review | `gpt-6.1-sol / medium` |
| difficult debugging, complex implementation, or high-risk review | `gpt-6.1-sol / high` |
| inventory, search, summaries, or verifiable mechanics | `gpt-6-luna / medium` |
| bounded documentation with multiple relationships to reconcile | `gpt-6-luna / high` |

This provisional, reversible, Yini-only directive records the owner's
2026-09-24 routing decision. Verify the exact model and reasoning tier are
available before dispatch. Do not reroute active tasks.
`gpt-5.6-terra` is an explicit owner-selected alternative, not a mandatory
tier; `gpt-6-luna / max` is not a default. Ambiguous classification or an
unavailable or inadequate route returns to the owner. Escalate substantive
semantic difficulty and repeated substantive failure, not shell, permission,
or harness symptoms alone. SDD depth does not determine a model. Insurance
coverage, exclusions, deductibles, and recommendations require source-grounded
evaluation and human review, not simple summary routing. Use existing receipts
for observed evidence; this directive is not a benchmark, savings claim,
action grant, or successor authority. Silent substitution is forbidden.

The owner approved on 2026-09-29 replacing `gpt-6-sol` with `gpt-6.1-sol` for
the two Sol routes, preserving their Medium/High reasoning tiers and work
classes. Astra and Luna defaults remain unchanged. This update applies to
future dispatches; do not reroute active tasks. `gpt-6-sol` remains an
explicitly selected alternative.

## Compact Gate Cadence

The normal cadence counts owner approval gates, not executor tasks. Level 0
normally uses two owner decisions. Level 1 or 2 with an accepted applicable
spec normally uses three; without the required spec it uses four. Level 3 adds
separate decisions for each provider, deployment, pilot, production, or other
external rung. Classified findings and stops are contingency decisions, not
hidden normal gates.

## Owner Gates and Lifecycle Bundles

Owner approval gates are not executor tasks. A grouped lifecycle decision may
name spec acceptance plus delivery, owner-disposed correction plus conditional
fresh review, or final acceptance plus separately named close/Git actions.
Each named grant keeps distinct task identity, fixed point or ordered successor
precondition, scope, stops, consumption, and receipt. Master control may
administratively dispatch an already-authorized task but may not perform this
executor work.

## Retry and Harness Contingencies

The following legacy conditional mechanical retry applies only when that exact
two-task mechanism is selected. It is separate from an explicitly selected
local objective bundle; neither mechanism borrows the other's counters or
converts an existing grant.

A mechanical retry bundle has exactly one primary invocation and one dormant
retry in a separately named fresh task, eligible only for the declared
pre-mutation invocation error after unchanged context is proven. A second
retry, third invocation, changed invocation, unknown state, Git, provider,
network, external, destructive, or target-changing failure is ineligible.

Generic retry or harness-repair language is not authority. A harness defect is
not a candidate finding or a retry. Under the legacy mechanism it requires a
separately scoped repair decision and owner disposition afterward, and it never
resumes candidate work automatically.

### Opt-In Local Objective Continuity

The owner may expressly select the installed plugin's
`references/authority-grants.md` local objective bundle for one fresh visible
executor task. It names separate implementation and validation grants and binds
the owner, work unit, executor, physical checkout/common-dir, HEAD/ref, index,
complete relevant candidate identity, measurable completion predicate, exact
path allowlist, mutation class, safe validator invocations, budgets, and stops.
Before consumption, prove all bound identity and relevant tracked, untracked,
ignored, and generated state. A mismatch expires the bundle. Each first
mutation or validation invocation consumes its named grant; only declared
successor steps may continue against their exact observed predecessor.

Within that still-current bundle, affected checks and scoped correction may
continue locally. Its distinct ceilings are two eligible identical-invocation
transient retries before target mutation, one invocation/environment-only
harness repair with unchanged oracle and governed inputs, and two executor
semantic correction cycles after first complete candidate validation. A
changed assertion, fixture meaning, oracle, acceptance criterion, or tested
semantics is semantic correction, never harness repair. Run affected checks
after edits and at most one declared final proportional local suite; a focused
PASS on unchanged candidate needs no ceremonial broad rerun.

Unknown or unrelated mutation, incomplete state coverage, deterministic repeat
failure, unsafe test, denied permission, network, dependency acquisition, Git,
provider or external action, sensitive data, exhausted balance, or material
scope change stops local continuation. Terminal bundles cannot be resumed.
Independent review, owner acceptance, Git, and external phases stay separate.
The plugin owns the detailed transition rules; this local pointer creates no
default or retroactive grant.

### Objective Preparation and Continuation — F2-O Adoption Candidate

CANDIDATE, 2026-10-01. This carries the F2-D guidance into a canonical
adoption candidate under the
[execution-fluency requirements R1–R4](../../specs/2026-09-30-execution-fluency-roadmap/requirements.md).
The owner accepted the F1 candidate after its narrow review and accepted its
controlled read-only integration after independent F1-LR review. This text
remains inactive until independent documentary review and owner acceptance of
these exact bytes. Until then, existing v1/v2 selection and exact dispatch
remain in force; this v1-only transport does not cover v2 or future v3.

For an eligible v1 request after that adoption gate, the canonical transport
pointer is [`scripts/execution_contract.py`](../../scripts/execution_contract.py).
Master supplies the closed owner-bound request, exact source bytes and
externally bound digests; the executor runs `prepare` first and invokes
`invoke` only for a valid `PREPARED` result, preserving the same request and
source identities. The transport delegates observation to the unchanged v1
observer and does not certify its own bootstrap. Unsupported coverage stops
before invocation. An invoked observer `STOP`, nonzero exit, invalid result,
or drift is terminal: no replay, repair, fallback or changed expectation.
The pointer adds no authority or runtime enforcement; the installed
`references/authority-grants.md` owns universal grant rules. V2 and future v3
remain on their separately selected mechanisms and contracts.

Master prepares exact source bytes and externally bound digests, native source
thread/turn/page/item pointers, complete protected inventory, runtime/tool
identities, checkout, objective, path scopes, safe validators, route, finite
counters and expected successors before dispatch. Executor checks these inputs
without reconstructing sessions, rebinding an oracle to observed state,
selecting another checkout or using the new mechanism to certify its bootstrap.
Deterministic preparation validates data; it does not authenticate authority
or establish runtime permission. Native final messages and complete command
items are evidence; reasoning is excluded and a selected complete item does
not establish complete thread history.

Only an expressly selected, still-current local objective bundle permits
declared edits, affected checks and finite correction in the same visible
executor task. Expected successor bytes and intended TDD RED-to-GREEN may
continue under their named grants without another mechanical confirmation.
Fresh independent review and owner acceptance remain separate; a grouped
decision names each authority and grants no standing or successor permission.
The installed `references/authority-grants.md` remains the universal owner.

The following proposed scenarios make the existing limits reviewable; they
are documentary examples, not a policy engine or runtime enforcement:

| Scenario | Continuation and accounting |
|---|---|
| Declared successor edit, intended TDD RED, then affected PASS | Continue within the same exact objective; intended RED uses no semantic correction counter |
| Eligible transient invocation failure before target mutation, context unchanged | Use only the expressly granted identical-invocation retry balance, ceiling 2; deterministic repeat stops |
| Invocation/environment construction fault before observer launch, oracle and governed input unchanged | Use only the expressly granted harness repair balance, ceiling 1; record the actual repair |
| Valid candidate finding after first complete candidate validation | Use only the expressly granted semantic correction balance, ceiling 2; then affected checks |
| Changed assertion, fixture meaning, expected hash, or authoritative literal | Semantic change requires its applicable authority; never classify it as invocation-only repair |
| Observer STOP/nonzero or invalid/missing result after launch | Terminal, with native capture retained; no replay, repair, fallback or changed expectation |
| Drift, unknown mutation, denial, sensitive data, unsafe test, scope conflict, expiry or exhausted balance | Terminal; preserve state and return owner decision, never restart the terminal bundle |
| Candidate complete under selected checks | Return READY_FOR_INDEPENDENT_REVIEW at the observed rung; no self-review, acceptance, Git or external action |

The 2/1/2 balances are independent and cannot transfer. A focused PASS on an
unchanged candidate adds no repeated broad suite. Retained read-only capture
may complete a missing authorized range without replaying its originating
operation. Literal/transcription correction is not newly eligible here;
F4's proposed clarification needs its own future disposition. No per-tool
receipt store, counter registry, automatic gate transition or efficiency claim
is introduced.

### Recoverable Read-Only Capture

Prospective amendment, 2026-09-17: 100 lines is an initial pagination target,
not a safety/acceptance invariant or a universal command/input limit. A
complete authorized output with its expected exit does not fail solely because
it exceeds that target. Presentation size is configurable in characters/tokens;
source/range identity, exit semantics, and completeness are separate evidence.
Use the sole [capture recipe and decision table](../../specs/2026-09-15-executor-checkout-boundary/plan.md#capture-size-amendment--2026-09-17)
for retained-output pagination, including long records, and actual total budgets.
Oversize alone does not classify an observation as facade `HARNESS_DEFECT`.

Truncated or incomplete read-only output remains `INCOMPLETE` until its missing
authorized ranges are captured within the same task's total allowance. Never
infer completeness from a line count. This amendment does not excuse a breach
of a historical explicit hard grant or turn a historical STOP into PASS. Future
master handoffs must bind presentation controls separately from actual total
budgets, rather than inventing a hard 100-line limit for every command.

This is continuation of the same read-only inspection, not a retry grant,
new task, or renewed authority. Never replay an originating mutation to
recover its output. An expected `rg` no-match exit or documented no-index
diff result is not automatically a tool failure; inspect output and command
semantics. Real state drift, write failure, unexpected non-capture tool error,
secret exposure risk, or scope conflict still stops under the original grant.

An exact source list distinguishes required from optional sources before the
read. A verified optional absence or no-match may be recorded and pruned from
the remaining capture only when the grant names an already-authorized bounded
alternative; it neither supplies missing content nor substitutes for a
required source. Keep the symptom, source/range, classification, continuation,
and remaining gap in the receipt. Required absence after the safe lookup, an
unbounded alternative search, or exhausted allowance stops.

For `read_thread` and similar wrappers, emit the response envelope before
parsing and classify the body fail-closed. This compact helper is a local
capture guard, not an official global response schema:

```js
function classifyReadThread(result, emit = console.log) {
  const objectResult = result && typeof result === "object" ? result : null;
  const blocks = Array.isArray(objectResult?.content) ? objectResult.content : [];
  const text = typeof result === "string"
    ? result
    : blocks.filter((b) => b?.type === "text" && typeof b.text === "string")
        .map((b) => b.text).join("\n");
  const envelope = {
    format: typeof result,
    isError: objectResult?.isError === true,
    blockTypes: blocks.map((b) => b?.type).filter(Boolean),
  };
  emit(envelope);
  if (envelope.isError) return { kind: "tool_error", complete: false };
  if (!text) return { kind: "missing_text", complete: false };

  let payload;
  try {
    payload = JSON.parse(text);
  } catch (error) {
    return {
      kind: /^\s*[\[{]/.test(text) ? "malformed_json" : "plain_text_error",
      complete: false,
      error: String(error),
    };
  }
  const isRecord = (value) => Boolean(value && typeof value === "object" &&
    !Array.isArray(value));
  const turns = payload?.turns;
  const items = payload?.items;
  const records = Array.isArray(turns) ? turns
    : Array.isArray(items) ? items : null;
  const traversable = Array.isArray(turns)
    ? turns.every((turn) => isRecord(turn) && Array.isArray(turn.items) &&
      turn.items.every(isRecord))
    : Array.isArray(items) && items.every(isRecord);
  if (!records || !traversable) {
    return { kind: "unexpected_shape", complete: false };
  }
  const incomplete = (value) => Boolean(value && typeof value === "object" &&
    (value.truncated === true || value.complete === false ||
      Object.values(value).some(incomplete)));
  if (payload.page?.hasMore === true || incomplete(payload)) {
    return { kind: "truncated", complete: false };
  }
  return { kind: "valid", complete: true, records };
}
```

Traverse `records` only after `kind: "valid"`. Returned errors never become
PASS, and truncated content never proves complete capture. Continue only the
missing authorized read-only range; never reconstruct content or replay an
originating mutation.

## CompactHandoff Selection

CompactHandoff is optional and explicit. When a grant does not select v3, use
a compact delta that states the fixed point, scope, exclusions, authority and
evidence limits, and stop conditions. A selected v3 transport fails closed
without fallback: an issue, version, manifest, or verification failure stops
that action for owner disposition.

CompactHandoff does not authenticate authority, prove manifest or Git truth,
consume a grant, prevent replay, accept bytes, or replace independent
preflight or Receipt Capsule v1. Local documents point to the installed
handoff skill and do not copy its code, schemas, references, fixtures, or
universal contract.

## Execution Rules

An executor must:

1. verify the physical checkout first under Checkout Boundary, then use the
   applicable owner-bound deterministic preflight before editing;
2. read the active spec, related modules, callers, exports, and tests;
3. preserve existing and foreign changes;
4. implement only documented behavior;
5. keep changes minimal and reversible;
6. run acceptance checks proportionate to risk;
7. keep canonical-document updates inside delivery before review;
8. avoid credentials, providers, deployment, network, Git mutation, and other
   excluded actions unless separately authorized;
9. stop on drift, undeclared foreign/generated state, sensitive-data risk,
   conflicts, invalid routing, unexpected non-capture failure, or material
   ambiguity; a harness defect may continue only under a still-current,
   expressly selected objective bundle after its unchanged-oracle guard passes;
   complete recoverable read-only capture as above;
10. avoid opening the next slice or making portfolio decisions.

## Return Contract

The executor must return:

- role, `dispatch_owner`, observed physical repository and absolute common-dir,
  and the required checkout precondition with its match/mismatch result;
- terminal state and task/fixed-point identity;
- exact files changed;
- exact staged delta, normally empty unless separately authorized;
- concise diff summary;
- commands executed with pass/fail results;
- skipped or unavailable checks;
- commit, ref, or external facts only when actually observed under authority;
- remaining risks, blockers, and the evidence ceiling;
- the next owner gate.

Return Receipt Capsule v1 without raw diffs, secrets, or unsupported claims.
Local tests cannot be reported as integration, provider, hosted, release,
deployment, pilot, production, or human acceptance evidence.

## Review and Acceptance

Formal independent review uses a fresh visible task that did not author the
candidate and is bound to the complete exact candidate. It returns findings or
PASS for owner disposition without correction or acceptance. The owner alone
accepts or rejects bytes. A clean diff, PASS, receipt, review, acceptance,
commit, or push never authorizes its successor.
