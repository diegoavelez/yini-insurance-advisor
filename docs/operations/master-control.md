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

`docs/agents/executor-workflow.md` owns the single provisional, local,
revocable, non-authorizing routing matrix. Ordinary Master Control orientation
uses `gpt-6-astra / medium`; architecture, transversal decisions, material
contradictions, and high-risk migrations use `gpt-6-astra / high`. The executor
matrix governs every other classification. Routing is the provisional,
reversible Yini-only owner decision of 2026-09-24; verify exact model and tier
availability before dispatch and do not reroute active tasks.

Ambiguous classification, an unavailable required route, or an inadequate
model/tier returns the decision to the owner. Silent substitution is forbidden.
The directive is not a benchmark, reusable quality evidence, a savings claim,
an execution grant, or successor authority.

## Visible Task Topology

Each executor objective and later independent review or lifecycle phase uses
a fresh visible task. An expressly owner-selected local objective bundle may
cover scoped implementation, affected validation, and finite correction in
one executor task under the installed plugin's `references/authority-grants.md`.
Previously issued action-specific grants keep their literal rules. Git,
publication, provider execution, deployment, pilot, production, and external
actions remain separate. Worktree selection creates no authority.

Master control alone dispatches those tasks under exact owner grants.
Executors perform the isolated task received; they never create, fork, hand
off, or send another task, or reselect their checkout. Reading this document
does not convert an executor into master control, and "fresh visible task"
does not instruct an executor to redelegate.

Yini uses the principal checkout by default. A worktree requires explicit
owner choice and a reason before dispatch. An executor that needs ungranted
isolation returns the need to the owner. Each handoff declares role,
`dispatch_owner`, physical repository, absolute common-dir, and checkout
precondition; the executor returns those fields with its observed match.
`docs/agents/executor-workflow.md` owns the physical preflight-first rule,
stop without corrective `cd`, contractual enforcement limits, and continued
read-only pagination for incomplete capture. Reading recovery neither creates
a new task nor renews any mutation authority; true failures retain their stops.

Internal subagents may support only at least two independent, bounded,
non-mutating analysis workstreams when additional coverage or wall time
justifies them. They never replace a visible lifecycle task.

## Gate Cadence

The cadence counts owner decisions, never executor-task volume. Each task still
has its own identity, preconditions, scope, stops, and Receipt Capsule.

## Owner Gate Budget

Owner approval gates are counted separately from executor tasks.

| SDD depth | Normal owner approval gates | Normal lifecycle |
|---|---:|---|
| Level 0 | 2 | proportional delivery/validation; acceptance with optional exact Git grants |
| Level 1 or 2 with an accepted applicable spec | 3 | spec acceptance plus delivery; independent review; final acceptance with optional close/Git grants |
| Level 1 or 2 without the required spec | 4 | specification candidate; then the accepted-spec lifecycle |
| Level 3 | Level 2 core plus external decisions | provider, deployment, pilot, production, and other external rungs remain separate |

Level 2 with an accepted applicable spec: 3 owner approval gates.
Contingencies are reported separately from the normal gate budget. An eligible
candidate finding or invocation-only harness defect may continue only within
an expressly selected, still-current local objective bundle and its guards and
budgets. Drift, validation gap, unavailable route, scope change, external rung,
and every ineligible or exhausted contingency return for classified owner
decision. These cases are not hidden inside the target count. This budget is
governance design, not measured token, latency, cost, quality, or productivity
evidence.

## Grouped Decisions and Administrative Dispatch

Grouped decisions retain separately named grants and receipts. One owner
decision may contain spec acceptance plus delivery, an owner-disposed
correction plus conditional fresh review, or final acceptance plus separately
named canonical-freeze, differential-review, staging, commit, and push grants.
Every contained action retains its task identity, fixed-point or successor
precondition, scope, stop conditions, consumption, and terminal result.

An opt-in local objective bundle is a distinct, explicitly selected form for
one executor objective, with separate implementation and validation grants.
Its finite local correction, retry, and harness budgets do not change the
legacy two-task conditional retry or prior literal grants. It never includes
independent review, owner acceptance, Git, provider, or external actions.

Master control may administratively dispatch only already-authorized visible
tasks. Dispatch realizes a current exact grant; it is not an additional owner
gate and does not permit the control tower to implement, validate, review,
accept, mutate Git, access providers, or perform external actions. An unnamed
task, changed fixed point, failed precondition, or scope expansion returns to
the owner.

No automatic post-Git documentary reconciliation occurs unless semantic state
changed. Git remains the live-fact owner.

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
