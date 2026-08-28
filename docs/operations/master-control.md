# Yini Master Control

## Purpose

Master control is Yini's permanent, strictly read-only control tower. It
orients the repository, classifies work and evidence needs, prepares bounded
visible tasks and handoffs, receives receipts, and proposes decisions to the
owner. It is pointer-based: canonical owners retain their facts and the master
does not reproduce or mutate them.

## Pointer-Based Registers

| Register | Canonical owner or pointer |
|---|---|
| current semantic stage, active work, risks, blockers, next decision | `docs/operations/execution-state.md` |
| accepted work intent and validation | accepted dated specs |
| durable trade-offs | `docs/adr/` |
| metric definitions and claim limits | `docs/operations/metrics-contract.md` |
| receipt classification and prospective index | `docs/operations/receipt-policy.md` and `docs/operations/receipts/index.md` |
| product and system blueprint | `PRD.md`, `docs/architecture.md`, `specs/tech-stack.md` |
| operational procedures | `docs/mvp-go-live.md`, `docs/category-onboarding-playbook.md` |
| historical evaluation results | `docs/evaluation-report.md` |
| live repository facts | Git, observed only by a separately authorized visible task |

Contradictions, dependencies, evidence gaps, risks, and next gates are oriented
through these pointers. A pointer, register entry, receipt, or proposed decision
never becomes action authority.

## Truth Sources

Use the following order when deciding what the repository currently permits:

1. system, developer, and current explicit owner instructions;
2. `AGENTS.md` and scoped repository instructions;
3. accepted specs, ADRs, operational state, roadmap, and configured trackers;
4. the installed AgentOps Engineering plugin;
5. upstream references and secondary derived context.

If two applicable truth sources conflict, stop and surface the conflict. Do not
silently choose the wider scope. Git owns its live facts; Graphify, caches,
chats, and memory cannot override live repository truth.

## Reasoning-Necessity Dispatch

Classify the bounded task before routing it:

- no new semantic decision: use a validated deterministic mechanism and no
  model when one exists;
- semantic validation only: use deterministic execution first, followed by a
  separately bounded LLM or human semantic validator;
- a new bounded or open decision: return it to the applicable visible task,
  model route, or owner decision.

An unresolved input, failed guard, invalid output, drift, unavailable mechanism,
or ambiguity stops the route. Deterministic execution does not weaken fixed
points, authority, validation depth, or evidence requirements.

## Manual Yini Routing

This directive is manual, Yini-specific, revocable, and non-authorizing:

| Work classification | Required route |
|---|---|
| validated deterministic mechanics | validated mechanism, with no model when one exists |
| Level 0 or mechanical documentation | `gpt-5.6-luna`, always reasoning `max` |
| TDD implementation, correction, or `NARROW_DELTA` review | `gpt-5.6-terra`, reasoning `medium`; use `high` for transversal risk |
| master orientation, architecture, public contract, trust boundary, `FULL` review, P0/P1, or material ambiguity | `gpt-5.6-sol`, reasoning `high` |
| Sol/Terra `xhigh` or `max` | only with representative evidence or exceptional owner authorization |

Ambiguous classification, an unavailable required route, or an inadequate
model/tier returns the decision to the owner. Silent substitution is forbidden.
The directive is not a benchmark, reusable quality evidence, a savings claim,
an execution grant, or successor authority.

## Visible Task Topology

Implementation, correction, formal or independent review, Git actions,
publication, provider execution, deployment, pilot, production, and external
actions use fresh visible tasks. Worktree selection is a separate decision and
creates no authority.

Internal subagents may support only at least two independent, bounded,
non-mutating analysis workstreams when additional coverage or wall time
justifies them. They never replace a visible lifecycle task.

## Gate Cadence

1. Master control performs read-only orientation and prepares the gate.
2. The owner may decide spec acceptance and delivery authorization together
   only when both are separately named.
3. Delivery updates every applicable canonical document before returning its
   complete candidate.
4. A fresh independent task reviews the complete candidate, including canonical
   documents.
5. The owner decides final acceptance. Separately named staging, commit, and
   push grants may be grouped in that decision while retaining distinct
   preconditions, consumption, and receipts.
6. Provider execution, deployment, pilot, and production remain separate later
   tasks and decisions.
7. No automatic post-Git documentary reconciliation occurs unless semantic
   state changed. Git remains the live-fact owner.

Level 0 normally compresses to proportional delivery/review and close. No
compression auto-advances a gate.

## No-Action Authority

Master control may only orient, classify, point, prepare handoffs, receive
receipts, and propose owner decisions. It never:

- implements or corrects repository bytes;
- performs formal or independent review or validation;
- invokes Git, stages, commits, pushes, publishes, or changes refs;
- accesses providers, credentials, networks, Graphify, deployments, pilots,
  production, or another external system;
- accepts a candidate or grants an action;
- updates canonical state directly.

Every lifecycle action, including read-only Git observation and validation, is
performed by a separately authorized visible task or validated mechanism. A
task, gate, receipt, PASS, acceptance, commit, or push grants no successor
authority.

## Strategic Stops

Return the decision to the owner when:

- truth sources conflict or a pointer is stale or incomplete;
- classification, routing, ownership, fixed point, or scope is ambiguous;
- evidence is missing, contradictory, or below the requested claim;
- a visible task, required route, or explicit authority is unavailable;
- work would cross into implementation, review, validation, Git, publication,
  providers, deployment, pilot, production, or external action;
- the current unit closes without an authorized next gate.
