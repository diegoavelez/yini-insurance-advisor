---
agentops_policy_version: "1.4"
profile: "provider-eval"
plugin_minimum_version: "0.9.0"
---

<!-- agentops-engineering:workflow:start -->
# AgentOps Workflow

## Universal Owners

The installed `agentops-engineering` plugin resource `references/OPERATING-MODEL.md` owns the universal execution contract. This file is a compact repository adapter and must not copy or override that contract.

Routine delegation applies the Operating Model directly. CompactHandoff is optional and explicit; when selected for a relevant boundary, `skills/handoff/SKILL.md` owns its specialized construction and verification contract. Neither this adapter nor routine delegation requires invoking that skill for every handoff.

## Sources of Truth

Use this precedence:

1. System, developer, and user instructions.
2. The target repository's `AGENTS.md` and scoped agent instructions.
3. Current repository specs, ADRs, operations state, roadmap, and configured tracker docs.
4. The AgentOps Engineering plugin.
5. Upstream reference material.

The plugin never overrides repository gates, decisions, authority, or current state.

The current repository sources for this adapter are:

- `docs/operations/execution-state.md`
- `docs/agents/executor-workflow.md`
- `docs/operations/master-control.md`

Master control detected at `docs/operations/master-control.md`; base setup links and preserves it but does not create or rewrite it.

Secondary indexes, generated graphs, and cached summaries cannot override these live sources.

## Repository Profile and Gates

Use the product profile plus explicit eval contracts, datasets, runners, evidence packages, and human-review protocols.

Use Level 0 for minor changes, Level 1 for small bounded slices, Level 2 for technical features, and Level 3 for services or production workflows. Repository-specific definitions override these defaults.

### Required profile gates

- controlled synthetic evidence
- separately authorized provider-backed execution with cost and data limits
- human review that automated evidence cannot replace

### Profile-specific rules

- Separate credentials from repo artifacts and redact logs.
- Zero or partial provider execution remains failed or incomplete evidence; never normalize it into readiness.

These profile rules and gates are repository-local. They add no central registry, rollout ledger, adoption manifest, durable handoff archive, fleet-wide apply state, or central live-state owner.

## Validation

Local validation is optional and must be selected and authorized explicitly. Declaring commands here does not run them and creates no validation, implementation, Git, installation, publication, or successor authority.

Selected repository commands:

- `make test-release`

## Feature Close

Stop after evidence acceptance to decide whether another eval rung, pilot, or a different product direction is permitted.

Record the evidence ceiling, residual risk, and next owner decision. Do not auto-start another feature or gate.
<!-- agentops-engineering:workflow:end -->
