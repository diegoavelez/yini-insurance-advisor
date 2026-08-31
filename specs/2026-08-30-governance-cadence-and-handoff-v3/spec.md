# Governance Cadence and CompactHandoff v3 Selection

## Status and Authority

- Work unit: `YINI-GOVERNANCE-CADENCE-AND-HANDOFF-V3`.
- Specification gate: `YINI-GOVERNANCE-CADENCE-AND-HANDOFF-V3-SPEC-1`.
- SDD depth: Level 2.
- Specification fixed point:
  `c603647d280049f8bb8a2afc0678e7065341fade`.
- Specification fixed-point tree:
  `cd5021944f6755f420e0678bc3131932738826e6`.
- This five-file package is a non-authorizing candidate for owner decision. It
  does not accept its own bytes or authorize delivery, correction, review,
  validation beyond this package, Git, plugin mutation, provider access,
  deployment, pilot, production, or another external action.

## Problem

Yini's accepted governance already permits grouped owner decisions, fresh
visible lifecycle tasks, proportional Level 0 work, and no automatic post-Git
reconciliation without semantic change. The last Level 2 governance slice
nevertheless required substantially more owner interactions and executor tasks
than its nominal lifecycle because owner-decision gates, executor-task
boundaries, contingencies, and administrative dispatch were not distinguished
precisely enough.

The repository also points to optional CompactHandoff behavior but does not
state when Yini selects machine-verifiable CompactHandoff v3 instead of a
bounded Markdown handoff. The installed plugin supports v3, while the adapter's
minimum version still predates it. This leaves high-risk task, review, retry,
and worktree boundaries vulnerable to oversized or incomplete handoff prompts
without making v3 universally appropriate.

## Outcome

Establish a repository-local operating contract that:

1. counts owner approval gates separately from executor tasks;
2. defines a normal owner-interruption budget by SDD depth;
3. names the grouped lifecycle decisions that reduce ceremonial approvals
   without merging authorities or auto-advancing tasks;
4. closes retry and harness contingencies consistently with the installed
   AgentOps authority contract;
5. selects CompactHandoff v3 only at boundaries where candidate binding and
   machine-verifiable transport materially reduce ambiguity;
6. updates the local validator and tests so the compact cadence cannot silently
   regress; and
7. preserves the strictly read-only master-control topology and all current
   evidence, Git, provider, and human-decision boundaries.

The normal gate budget is a governance target, not measured evidence of token,
latency, cost, quality, or delivery improvement.

## Users

- The owner, who should see only decisions that require human authority or
  disposition.
- Master control, which prepares exact gates and dispatches already authorized
  visible tasks without repeatedly asking for the same decision.
- Delivery, correction, review, Git, and external executors, which need bounded
  task identities, fixed points, paths, validators, stops, and receipts.
- Future maintainers of the repository-local AgentOps adapter and validator.

## Canonical Terms

- **Owner approval gate:** one owner decision that accepts, rejects, authorizes,
  or disposes named work. It may contain separately named grants but is not an
  executor task.
- **Executor task:** one fresh visible task performing one lifecycle phase or
  action under a bounded grant. Multiple executor tasks may be named in one
  explicit owner decision while retaining independent preconditions and
  receipts.
- **Normal gate budget:** the expected count of owner approval gates for an
  uncomplicated work unit at a declared SDD depth.
- **Contingency gate:** an additional owner decision caused by a classified
  finding, drift, harness defect, validation gap, unavailable required route,
  or another stop condition. It is not silently normalized into the budget.
- **Lifecycle bundle:** one owner decision containing separately named grants,
  task identities, fixed points or ordered successor preconditions, scopes,
  stops, and terminal receipts. A bundle does not merge authorities.
- **Administrative dispatch:** creation or continuation of a task already named
  inside a valid unconsumed grant. It realizes existing authority and is not a
  new owner approval gate.
- **CompactHandoff v3:** optional candidate-bound context transport produced by
  the installed plugin's `issue()` seam and checked through `verify()`. It
  transports declared context only and creates no authority or observed Git
  truth.
- **Plain compact handoff:** a bounded Markdown or task prompt that satisfies
  the repository handoff contract without machine-verifiable v3 transport.

## Sources and Precedence

Use the repository precedence already established by `AGENTS.md` and
`docs/operations/master-control.md`. In particular:

1. current system, developer, and explicit owner instructions;
2. repository instructions and accepted local specs/ADRs/state;
3. the installed AgentOps Engineering Operating Model and its specialist
   authority and handoff contracts; and
4. upstream or derived context.

This package points to the installed plugin. It must not copy the universal
Operating Model, authority contract, CompactHandoff schema, script, fixtures,
or skill into the repository.

## Settled Decisions

### SDD owner-interruption budget

The normal budget counts owner approval gates, not visible tasks:

| SDD depth | Normal owner approval gates | Normal lifecycle |
|---|---:|---|
| Level 0 | 2 | authorize proportional delivery/validation; accept and optionally authorize exact Git grants |
| Level 1 with accepted spec | 3 | accept spec plus delivery; authorize independent review; accept plus optional Git bundle |
| Level 1 without spec | 4 | create spec candidate; then the three-gate accepted-spec lifecycle |
| Level 2 with accepted five-file package | 3 | accept spec plus delivery; authorize independent `FULL`; accept plus optional close/Git bundle |
| Level 2 without package | 4 | create five-file package; then the three-gate accepted-package lifecycle |
| Level 3 | Level 2 core plus required external rungs | keep provider, deployment, pilot, production, and other evidence-dependent actions separate |

Level promotion, a missing accepted spec, an independent finding, or an
external evidence rung changes the applicable lifecycle and must be reported;
it is not evidence that the normal budget failed.

### Grouped decisions

The repository-local projection permits these grouped decisions when every
grant is separately named and its preconditions are exact:

1. accepted-spec decision plus delivery grant;
2. a correction grant plus a conditional fresh `NARROW_DELTA` review grant
   after owner disposition of review findings;
3. final owner acceptance plus any exact canonical-freeze, differential-review,
   staging, commit, and push grants required for close; and
4. a primary invocation plus exactly one dormant mechanical retry grant under
   the universal conditional-retry rules.

Unexpected intermediate state terminates the applicable attempt. Grouping
does not authorize repair, cleanup, scope expansion, external evidence, or a
later semantic work unit.

### Administrative dispatch

Once the owner has issued an exact bundle, master control may create, title,
route, and dispatch the fresh visible tasks already named by that bundle and
may wait for their receipts. It must not ask for another owner approval merely
to create the task. A task not named by the grant, a changed fixed point, a new
semantic decision, or a failed precondition returns to the owner.

This does not expand master control into implementation, review, validation,
Git, provider, deployment, pilot, production, or acceptance activity.

### Retry and harness policy

- A mechanical retry bundle contains exactly two grants: one primary and one
  dormant retry in a distinct predeclared task identity.
- The dormant retry is eligible only for the declared invocation-error class
  before target mutation with the complete execution context proven unchanged.
- A second retry, third attempt, changed invocation, unknown mutation, Git,
  provider/network action, or target-changing failure is ineligible.
- A harness defect is not a candidate finding or mechanical retry. It requests
  a separately scoped repair decision and owner disposition afterward.
- No generic phrase such as “retries if needed” or “repair the harness if
  needed” is sufficient authority.

### CompactHandoff v3 selection

Yini uses the smallest safe handoff mechanism:

| Boundary | Yini selection |
|---|---|
| Level 0 or deterministic same-checkout Git mechanics | plain compact handoff |
| Level 1 without worktree, retry, long-context, or candidate-binding risk | plain compact handoff by default |
| Level 1 crossing a worktree, retry, long-context, or exact candidate boundary | CompactHandoff v3 |
| Level 2/3 delivery candidate to independent review | CompactHandoff v3 |
| Level 2/3 correction candidate to `NARROW_DELTA` or renewed `FULL` | CompactHandoff v3 delta handoff |
| Any governed worktree transfer or candidate-bound retry where v3 can represent the boundary | CompactHandoff v3 |
| Provider, deployment, pilot, production, or other external action | v3 may transport context, but the external grant remains separate |

New Yini issuance uses `handoff.v3`. At a boundary where this contract requires
v3, unavailable issuance/verification, manifest ambiguity, version mismatch,
or verification failure stops for owner disposition. There is no silent v2,
plain-text, regenerated, or alternate-transport fallback.

`local-pointer` remains the default transport and `portable-inline` is
explicit-only. The v3 artifact belongs in the OS temporary directory, not the
repository, unless a later owner explicitly authorizes a durable artifact.

### CompactHandoff trust ceiling

V3 structure, canonical bytes, binding, and manifest equality prove only the
declared transport relation. The executor independently observes its actual
root, Git state, candidate inventory, paths, validators, and environment.
CompactHandoff does not authenticate an owner or grant, prove manifest truth,
consume authority, prevent replay, accept bytes, or replace Receipt Capsule v1.

### Version selection

The future delivery raises the repository adapter's
`plugin_minimum_version` to `0.11.0`, the first local minimum that supports the
selected v3 contract. It does not pin a cache-build suffix, modify the installed
plugin, or create a repository-local wrapper around plugin internals.

## Interfaces and Consumers

The future delivery updates these local owners:

- `docs/operations/master-control.md`: canonical gate-budget, grouped-decision,
  dispatch, and stop semantics;
- `docs/agents/executor-workflow.md`: executor-facing cadence, contingency, and
  handoff selection rules;
- `docs/agents/agentops-workflow.md`: adapter minimum version and concise local
  v3 selection pointer;
- `docs/operations/execution-state.md`: current semantic work and next owner
  decision during delivery/close;
- `docs/adr/0002-owner-interruption-budget-and-compacthandoff-v3.md`:
  durable trade-off record;
- `scripts/validate_master_control.py` and
  `tests/test_validate_master_control.py`: deterministic enforcement; and
- `CHANGELOG.md`: delivered repository change before final review.

`AGENTS.md` already points to these owners and remains unchanged unless a
future fixed-point conflict proves that the always-loaded kernel is incomplete.

## Future Delivery Scope

The accepted five spec files remain governed read-only inputs during delivery.
The delivery mutation allowlist is:

- `CHANGELOG.md`
- `docs/operations/master-control.md`
- `docs/operations/execution-state.md`
- `docs/agents/executor-workflow.md`
- `docs/agents/agentops-workflow.md`
- `docs/adr/0002-owner-interruption-budget-and-compacthandoff-v3.md` (new)
- `scripts/validate_master_control.py`
- `tests/test_validate_master_control.py`

The complete review candidate is the five accepted spec files plus those eight
delivery paths. Any omitted applicable path or extra path is a scope conflict.

## Human Review

- The owner accepts or rejects this spec package.
- A future delivery returns one complete candidate without self-acceptance.
- A fresh independent `FULL` review evaluates Standards -> Spec -> Evidence ->
  Operations.
- Findings return to owner disposition. Any authorized correction and
  subsequent review use fresh visible tasks.
- Final owner acceptance remains distinct from the Git grants it may group.

## Security and Data Boundaries

- Handoffs and receipts contain no secrets, credentials, raw provider payloads,
  sensitive logs, or unsupported claims.
- The spec and delivery are local, deterministic, network-free, and
  provider-free.
- V3 redaction declarations do not replace source-data review or exhaustive
  data-loss prevention.
- No provider, deployment, pilot, production, Graphify, marketplace, or remote
  publication state is observed or changed by this work unit.

## Compatibility and Migration

- Preserve AgentOps policy `1.4` and repository profile `provider-eval`.
- Preserve the strictly read-only master-control topology and fresh visible
  lifecycle tasks.
- Preserve manual Yini model routing, including Luna at reasoning `max`.
- Do not rewrite the accepted
  `specs/2026-08-28-repository-governance-stabilization/` package or historical
  receipts.
- Replace vague local retry language only in current canonical owners and
  validator fixtures; do not rewrite historical task transcripts.
- Keep the local adapter pointer-based and smaller than the universal plugin
  contract.
- Do not claim measured gate, token, latency, quality, or cost improvement from
  the historical audit or this implementation.

## Non-Goals

- Implementing the governance delivery in this specification gate.
- Making CompactHandoff mandatory for every task or Level 0 work.
- Copying or modifying plugin code, schemas, references, skills, fixtures, or
  installed caches.
- Creating a repository-local CompactHandoff wrapper, registry, store, archive,
  CLI, observer, router, network integration, or orchestrator.
- Automatically accepting specs, candidates, findings, retries, repairs, Git,
  providers, deployments, pilots, production, or successor work.
- Measuring or claiming productivity, cost, latency, token, or quality savings.
- Changing product, RAG, Qdrant, data, dependencies, runtime, deployment, or
  provider behavior.
- Backfilling historical receipts or reconstructing prior task artifacts.

## Failure Modes and Stops

Stop fail-closed on fixed-point drift, foreign state, ambiguous scope, truth
conflict, missing accepted spec, unavailable required route, plugin version
below the accepted minimum, v3 issue/verify failure at a required boundary,
incomplete manifest observation, sensitive-data risk, validator harness defect,
unexpected RED, missing canonical owner, allowlist expansion, or evidence
overclaim.

No spec PASS, task creation, v3 verification, receipt, gate budget, retry
eligibility, review result, acceptance, commit, or push authorizes its
successor. No repair, cleanup, retry, fallback, staging, Git, provider, or
external action is implied by this candidate.
