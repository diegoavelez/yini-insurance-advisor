# Repository Governance Stabilization

## Status and Authority

- Work unit: `YINI-GOVERNANCE-STABILIZATION`.
- Specification gate: `YINI-GOVERNANCE-STABILIZATION-SPEC-1`.
- SDD depth: Level 2.
- Specification fixed point:
  `b1f1e49f6aab0672e7d34e7b3fabbf5629e82c0a`.
- This package is a non-authorizing candidate for owner decision. It does not
  accept its own bytes or authorize delivery, correction, independent review,
  validation beyond this package, Git mutation, publication, provider access,
  deployment, pilot, production, or any external action.

## Objective

Stabilize Yini's repository-local governance contract so that control,
execution, evidence, fact ownership, routing, and gate cadence have one
coherent local projection of the AgentOps Engineering Operating Model. The
future delivery must remove contradictions without copying the universal
contract into the repository and must leave strategy and successor authority
with the owner.

## Canonical Terms

- **Owner:** the human decision-maker who accepts or rejects candidates and
  issues explicit, bounded authority grants.
- **Master control:** the permanent, strictly read-only control tower. It
  orients, classifies, prepares visible tasks and handoffs, receives receipts,
  and proposes decisions.
- **Visible task:** a fresh Codex task/thread exposed in the task UI and bound
  to one lifecycle action, fixed point, scope, authority, and return contract.
- **Executor:** the visible task performing one authorized bounded action.
- **Internal subagent:** a non-visible supporting analysis worker. It is not an
  executor task and cannot satisfy a fresh-task boundary.
- **Delivery candidate:** the complete bounded set of repository bytes returned
  by an authorized delivery executor for independent review and owner decision.
- **Independent review:** a formal review in a fresh visible task that did not
  author the candidate and evaluates the complete candidate at its exact fixed
  point.
- **Canonical document:** a repository artifact that owns a declared durable
  semantic concern. It is not a substitute for Git or an external system's
  live state.
- **Evidence ceiling:** the highest evidence rung actually passed; it is a
  claim boundary, not authority.
- **Receipt:** a compact terminal record of observed work and evidence. A
  receipt grants nothing and does not become current state merely by existing.
- **Gate:** an owner decision boundary. A gate does not auto-advance its
  successor.

## Precedence

Conflicts are resolved in this order:

1. system, developer, and current explicit owner instructions;
2. `AGENTS.md` and scoped repository instructions;
3. accepted specs, ADRs, operational state, roadmap, and configured tracker
   documents;
4. the installed AgentOps Engineering plugin;
5. upstream references and secondary derived context.

Live Git state overrides documentary copies of transient Git facts. Graphify,
caches, chats, and memory are secondary and cannot override live repository
truth. Any material conflict or ambiguity stops work for owner disposition.

## Settled Decisions

### Read-only master topology

Master control may inspect read-only state, orient the work, classify the next
gate, prepare bounded handoffs, receive executor receipts, and propose owner
decisions. It must never perform implementation, correction, formal or
independent review, validation, Git mutation or transport, publication,
provider-backed execution, deployment, pilot, production, or another external
action.

Implementation, correction, independent review, Git actions, and external
actions require fresh visible tasks. A visible task and a worktree are separate
choices; neither creates authority.

An internal subagent may be used only to support at least two independent,
bounded, non-mutating analysis workstreams when the additional coverage or wall
time justifies it. It cannot replace any required visible task.

### Local SDD levels

| Level | Local meaning | Normal lifecycle |
|---|---|---|
| 0 | Tiny wording, date, rename, or mechanical documentation correction with no durable semantic decision | proportional delivery/review and close |
| 1 | Small bounded operational slice | one operational spec from purpose through decision |
| 2 | Technical feature or transversal repository contract | `spec.md`, `requirements.md`, `plan.md`, `tasks.md`, and `validation.md` |
| 3 | Service or production workflow | Level 2 plus blueprint, runbook, metrics, ADRs, eval evidence, contracts, workflows, or traces as applicable |

Public contracts, trust boundaries, transversal topology, integrations,
persistence, production behavior, and similarly durable surfaces promote the
required depth. This work is Level 2 because it changes a transversal
repository governance contract; its delivery may add the specifically required
ADR and operational contracts without promoting the package to a new product
feature.

### Fact ownership

| Fact class | Canonical owner | Repository projection rule |
|---|---|---|
| branch, `HEAD`, index, worktree, refs, remotes, divergence, tracking | Git | observe live; do not copy transient values into `execution-state` |
| external provider or hosting state | owning external system | record only dated historical observations in evidence/receipts |
| current semantic work, accepted local evidence, risks, blockers, next decision | `docs/operations/execution-state.md` | keep compact and semantic; point to Git when a live fact is needed |
| permanent coordination and authority boundaries | `docs/operations/master-control.md` | describe the read-only control tower and separate authorities |
| executor handoff and return behavior | `docs/agents/executor-workflow.md` | define the repository-local visible-task projection |
| durable trade-offs | ADRs | record why the decision exists, without becoming live state |
| intended work behavior | accepted specs | bind scope and acceptance, never successor authority |
| selected history | append-only receipts | compact, sanitized, non-authorizing history |
| current product/system blueprint | `PRD.md`, `docs/architecture.md`, `specs/tech-stack.md` | preserve and cross-link; do not create a duplicate blueprint |
| operating procedures | `docs/mvp-go-live.md`, `docs/category-onboarding-playbook.md` | preserve as runbooks; do not create duplicate runbooks |
| historical evaluation results | `docs/evaluation-report.md` | evidence history only; it is not the metrics contract |

### Compact gate cadence

1. Master control performs read-only orientation and prepares the gate.
2. The owner may combine acceptance of an accepted spec with authorization of
   its delivery in one decision, but the decision must name both separately.
3. Delivery occurs in a fresh visible task and must update every applicable
   canonical document before returning the complete candidate.
4. Independent review occurs in another fresh visible task and evaluates the
   complete candidate, including canonical-document updates.
5. The owner decides final acceptance. Separately named staging, commit, and
   push grants may be bundled with that decision, but each retains its own
   scope, preconditions, consumption, and terminal result.
6. Provider execution, deployment, pilot, and production remain separate later
   decisions and tasks.
7. No automatic post-Git documentary reconciliation is required unless the Git
   action changes semantic state. Git remains the owner of transient Git facts.

Level 0 normally compresses this to proportional delivery/review and close.
Compression never converts a result into successor authority.

### Manual Yini routing directive

This routing is repository-specific, manual, revocable, and subordinate to
scope, fixed-point, validation, and fresh-task controls.

| Work classification | Required route |
|---|---|
| validated deterministic mechanics | validated mechanism, with no model when one exists |
| Level 0 or mechanical documentation | `gpt-5.6-luna`, reasoning `max` |
| TDD implementation, correction, or `NARROW_DELTA` review | `gpt-5.6-terra`, reasoning `medium`; use `high` for transversal risk |
| master orientation, architecture, public contract, trust boundary, `FULL` review, P0/P1, or material ambiguity | `gpt-5.6-sol`, reasoning `high` |
| Sol/Terra `xhigh` or `max` | only with representative evidence or exceptional owner authorization |

If classification is ambiguous, or the required model/tier is unavailable or
inadequate, return the routing decision to the owner. Silent substitution is
forbidden. This directive is not a benchmark, reusable quality evidence, a
savings claim, an execution grant, or successor authority.

## Delivery Scope

The future delivery must evaluate applicability and then bind its candidate to
the following minimal allowlist. An omitted applicable path or any additional
path is a scope conflict requiring owner disposition.

- `AGENTS.md`
- `CHANGELOG.md`
- `docs/operations/master-control.md`
- `docs/operations/execution-state.md`
- `docs/agents/executor-workflow.md`
- `docs/operations/metrics-contract.md` (new)
- `docs/operations/receipt-policy.md` (new local projection)
- `docs/operations/receipts/index.md` (new append-only index)
- `docs/adr/0001-read-only-master-control-topology.md` (new)
- `scripts/validate_master_control.py`
- `tests/test_validate_master_control.py` (new if no equivalent validator test
  owner exists at the delivery fixed point)

The delivery must not modify `docs/agents/agentops-workflow.md` merely to copy
universal behavior. It must not create another blueprint, go-live runbook, or
category-onboarding runbook while the existing owners listed above cover those
functions. It must not backfill historical receipts or manufacture evidence.

## Documentation Gap and Coverage

Already covered:

- product and system blueprint: `PRD.md`, `docs/architecture.md`, and
  `specs/tech-stack.md`;
- go-live and category procedures: `docs/mvp-go-live.md` and
  `docs/category-onboarding-playbook.md`;
- historical evaluation evidence: `docs/evaluation-report.md`;
- universal execution, authority, convergence, and receipt invariants: the
  installed AgentOps Engineering plugin.

Missing or requiring local stabilization:

- an explicitly read-only master-control topology;
- semantic-only execution state with transient Git facts removed;
- the local fresh-visible-task projection and subagent boundary;
- a local metrics contract distinct from historical results;
- a local receipt classification/retention projection and append-only index;
- an ADR explaining the read-only topology;
- a validator and tests that reject the known contradictions.

## Compatibility and Migration

- Preserve the `provider-eval` profile and AgentOps policy `1.4` adapter.
- Treat current master-control language that assigns execution or validation to
  the master as migration input, not accepted target behavior.
- Remove live branch, `HEAD`, index, worktree, refs, remotes, divergence, and
  tracking values from the target execution-state schema. Historical external
  observations may remain only when dated and clearly non-current.
- Preserve meaningful accepted evidence, risks, blockers, and next decisions
  while eliminating transient Git snapshots and unsupported readiness claims.
- Update validator schema/markers and tests atomically with the new contract;
  do not preserve contradictory markers solely for backward compatibility.
- Do not rewrite historical specs or receipts. New local receipt artifacts
  begin prospectively and point to universal policy rather than duplicating it.
- Existing blueprint and runbook owners remain compatible and are cross-linked
  only when necessary.

## Out of Scope

- Implementing any governance change in this specification gate.
- Accepting, staging, committing, pushing, publishing, or merging this package.
- Modifying the installed plugin or copying its universal contract locally.
- Network, provider, Graphify, credential, deployment, pilot, production, or
  other external activity.
- Creating or repairing receipts for historical work.
- Product behavior, RAG behavior, data, dependencies, environments, caches, or
  ignored artifacts.

## Stops

Stop fail-closed on any fixed-point drift, dirty or foreign state outside the
authorized candidate, truth-source conflict, ambiguous routing, unavailable or
inadequate required model, sensitive-data risk, allowlist expansion, validator
harness defect, incomplete evidence, or attempt to infer successor authority.
No repair, cleanup, retry, substitution, staging, or follow-on gate is implied.
