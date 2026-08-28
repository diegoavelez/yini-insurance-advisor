<!-- agentops-engineering:start -->
## AgentOps Engineering Workflow

- Read `docs/agents/agentops-workflow.md` for this repository's profile, truth sources, validation commands, and local gate conventions.
- Apply AgentOps policy `1.4` with repository profile `provider-eval`.
- Read the installed `agentops-engineering` plugin resource `references/OPERATING-MODEL.md`; it is the canonical universal contract and this marker does not copy it.
- Routine delegation applies the Operating Model directly. CompactHandoff is optional and explicit; when it is relevant, `skills/handoff/SKILL.md` owns its specialized contract.
- A task, gate, handoff, acceptance, or receipt creates no standing authority and never auto-advances another action or evidence rung.
- Use only invented, public, or explicitly authorized data and report only the evidence rung actually reached.
- At an accepted feature boundary, follow this repository's feature-close convention before starting another feature.
<!-- agentops-engineering:end -->

# AGENTS.md

These rules apply to every task unless explicitly overridden.

## Repository Governance

- `docs/operations/master-control.md` defines a strictly read-only control
  tower. It orients, classifies, prepares visible tasks and handoffs, receives
  receipts, and proposes owner decisions; it performs no lifecycle action.
- `docs/operations/execution-state.md` owns current semantic work, accepted
  evidence, risks, blockers, and the next owner decision. Git exclusively owns
  live branch, `HEAD`, index, worktree, refs, remotes, and divergence facts.
- `docs/agents/executor-workflow.md` owns visible-task boundaries, the manual
  Yini routing directive, compact gate cadence, and executor returns.
- Implementation, correction, independent review, Git, provider, deployment,
  pilot, production, and external actions require fresh visible tasks and
  separately named authorities. Internal subagents never replace them.
- `docs/operations/metrics-contract.md` owns metric definitions;
  `docs/operations/receipt-policy.md` and
  `docs/operations/receipts/index.md` own the local receipt projection and
  prospective index. Universal policy remains in the installed plugin.
- Treat Graphify as secondary context. Stop fail-closed on drift, foreign
  changes, sensitive-data risk, truth conflict, unavailable required routing,
  or material scope ambiguity.

## Core Behavior

- Think before coding.
- For non-trivial tasks, write a short plan before editing.
- Prefer simple, minimal, reversible changes.
- Touch only files required by the task.
- Read related modules, callers, exports, and existing utilities before changing code.
- Match existing conventions over personal preference.
- Surface uncertainty, skipped checks, conflicts, and risks explicitly.
- Do not claim completion unless the work is verified.

## Spec-Driven Development

- Specs are the source of truth for non-trivial work.
- Use Level 0 for tiny mechanical changes, Level 1 for small operational
  slices, Level 2 for technical or transversal contracts, and Level 3 for
  service or production workflows. Repository specs may promote depth.
- Do not implement undocumented behavior.
- Map implementation to acceptance criteria.
- If specs conflict with code, stop and explain the conflict.
- Deliver work in small verifiable phases.

## Environment

- Use local `.venv` for development.
- Initialize repo with git
- Never install dependencies globally.
- Use `requirements.txt` or `pyproject.toml` as dependency source of truth.
- Docker is for reproducibility and deployment, not the primary local dev loop.

## Planning Rules

Enter planning mode when the task involves:
- 3+ steps;
- multiple files;
- architectural decisions;
- production-impacting behavior;
- unclear requirements.

A plan must include:
- objective;
- affected files;
- assumptions;
- risks;
- verification strategy.

If execution diverges, stop and re-plan.

## Verification

Before marking work complete:
- run relevant tests;
- run linters/type checks when available;
- verify behavior manually when needed;
- report commands executed;
- report files changed;
- report skipped checks.

Tests should verify intent, not only implementation details.

## Bug Fixing

- Find root causes before patching symptoms.
- Use logs, failing tests, stack traces, and CI output.
- Prefer the smallest safe fix.

## Documentation

- Durable project knowledge belongs in `docs/`, `specs/`, `decisions/`, or `tasks/lessons.md`.
- Update `tasks/lessons.md` only for repeated mistakes or project-specific lessons.
- Keep documentation useful, not noisy.

## Definition of Done

A task is done only when:
- it matches the spec;
- acceptance criteria are satisfied;
- relevant checks pass;
- assumptions and risks are reported;
- no important step was skipped silently.
