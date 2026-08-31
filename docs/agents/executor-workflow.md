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

## Internal Subagents

An internal subagent is support, not a visible task. It may be used only for at
least two independent, bounded, non-mutating analysis workstreams when focused
coverage or wall time justifies it. It never substitutes for a lifecycle task,
retry, implementation, correction, review, Git action, or external action.

## Handoff Contract

Every executor handoff must state:

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
| Level 0 or mechanical documentation | `gpt-5.6-luna`, always reasoning `max` |
| TDD implementation, correction, or `NARROW_DELTA` review | `gpt-5.6-terra`, reasoning `medium`; use `high` for transversal risk |
| master orientation, architecture, public contract, trust boundary, `FULL` review, P0/P1, or material ambiguity | `gpt-5.6-sol`, reasoning `high` |
| Sol/Terra `xhigh` or `max` | only with representative evidence or exceptional owner authorization |

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

## CompactHandoff Selection

Use the smallest safe handoff: Level 0 and deterministic same-checkout Git
mechanics use plain compact Markdown; Level 1 uses v3 only for a worktree,
candidate-bound retry, long-context, or exact candidate boundary. Level 2/3
delivery to independent review requires `handoff.v3`; Level 2/3 correction to
`NARROW_DELTA` or renewed `FULL` requires a v3 delta handoff. New Yini issuance
uses `handoff.v3` with `local-pointer` by default.

A required v3 issue, version, manifest, or verification failure stops for
owner disposition without fallback. CompactHandoff does not authenticate
authority, prove manifest or Git truth, consume a grant, prevent replay,
accept bytes, or replace independent preflight or Receipt Capsule v1. Local
documents point to the installed handoff skill and do not copy its code,
schemas, references, fixtures, or universal contract.

## Execution Rules

An executor must:

1. run a live Git preflight before editing;
2. read the active spec, related modules, callers, exports, and tests;
3. preserve existing and foreign changes;
4. implement only documented behavior;
5. keep changes minimal and reversible;
6. run acceptance checks proportionate to risk;
7. keep canonical-document updates inside delivery before review;
8. avoid credentials, providers, deployment, network, Git mutation, and other
   excluded actions unless separately authorized;
9. stop on drift, foreign/generated state, sensitive-data risk, conflicts,
   invalid routing, harness defect, unexpected failure, or material ambiguity;
10. avoid opening the next slice or making portfolio decisions.

## Return Contract

The executor must return:

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
