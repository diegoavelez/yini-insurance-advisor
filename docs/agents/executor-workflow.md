# Executor Workflow

## Purpose

Executor tasks perform one bounded lifecycle action under an explicit owner
grant. They do not act as master control, choose the next strategic unit,
self-review formally, self-accept, or inherit successor authority.

## Visible Task Topology

Implementation, correction, formal or independent review, Git actions,
publication, provider execution, deployment, pilot, production, and external
actions use fresh visible Codex tasks. Task and worktree selection are separate;
neither creates authority.

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
Then verify the granted branch/HEAD, index, inventory, bytes, and modes.
Explicitly inventoried owner-permitted foreign changes remain untouched and
do not require a clean working tree; any undeclared delta still stops.

These rules are contractual controls, not hard enforcement. No per-task
tool-allowlist schema has been demonstrated for this boundary. Do not claim
tools were removed or change Codex, plugin, cache, or marketplace configuration
to implement this documentary rule.

## Closed Recipe and Bounded Recovery

The accepted executor-and-checkout-boundary specification is a historical
specification decision, not acceptance of any delivery bytes or authority to
run a later stage. Its
[`plan.md`](../../specs/2026-09-15-executor-checkout-boundary/plan.md) is the
sole local owner of the closed read-only recipe, its literal invocation order,
and its transition graph. A future task may use that recipe only when its fresh
grant binds the complete inputs, paths, sources, bounds, and selected checks.
This workflow points to that canonical plan; it does not copy its recipe,
graph, parser, or universal contract.

Before review, a delivery task using that plan updates the applicable canonical
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
| architecture, irreversibility, cross-repository implications, contradictions, or repeated substantive failures | `gpt-6-astra / high` |
| complex implementation or difficult debugging | `gpt-5.6-sol / high` |
| bounded implementation, tests, or refactors | `gpt-5.6-terra / high` |
| search, inventory, summaries, or verifiable mechanical documentation | `gpt-5.6-luna / max` |

Ambiguous classification, unavailable routes, or inadequate model/tier returns
to the owner. Silent substitution is forbidden. This manual, Yini-specific,
revocable directive is not a benchmark, reusable evidence, savings claim,
action grant, or successor authority.

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

A mechanical retry bundle has exactly one primary invocation and one dormant
retry in a separately named fresh task, eligible only for the declared
pre-mutation invocation error after unchanged context is proven. A second
retry, third invocation, changed invocation, unknown state, Git, provider,
network, external, destructive, or target-changing failure is ineligible.

Generic retry or harness-repair language is not authority. A harness defect is
not a candidate finding or a retry: it requires a separately scoped repair
decision and owner disposition afterward, and it never resumes candidate work
automatically.

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

1. verify the physical checkout first under Checkout Boundary, then run the
   remaining live Git preflight before editing;
2. read the active spec, related modules, callers, exports, and tests;
3. preserve existing and foreign changes;
4. implement only documented behavior;
5. keep changes minimal and reversible;
6. run acceptance checks proportionate to risk;
7. keep canonical-document updates inside delivery before review;
8. avoid credentials, providers, deployment, network, Git mutation, and other
   excluded actions unless separately authorized;
9. stop on drift, undeclared foreign/generated state, sensitive-data risk,
   conflicts, invalid routing, harness defect, unexpected non-capture failure,
   or material ambiguity; complete recoverable read-only capture as above;
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
