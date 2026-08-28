# Validation

## Evidence Ceiling

This specification gate can reach only evidence rung 1: static/schema evidence
over the five new Markdown files. It does not validate or implement repository
governance and does not prove independent review, Git integration, provider,
deployment, pilot, production, or human acceptance.

A future delivery can reach at most rung 2 after focused deterministic tests and
local validators pass. Later rungs require separately authorized evidence.

## Specification-Gate Allowlist

Exactly these paths may be new or modified in this gate:

```text
specs/2026-08-28-repository-governance-stabilization/spec.md
specs/2026-08-28-repository-governance-stabilization/requirements.md
specs/2026-08-28-repository-governance-stabilization/plan.md
specs/2026-08-28-repository-governance-stabilization/tasks.md
specs/2026-08-28-repository-governance-stabilization/validation.md
```

No staged path is permitted. No generated, ignored, cache, environment, Git,
network, provider, Graphify, or cleanup artifact is permitted.

## Specification-Gate Checks

Run from repository root, without staging the new files:

```bash
git rev-parse HEAD
git rev-parse --git-common-dir
git diff --cached --quiet
git status --porcelain=v1 --untracked-files=all
find specs/2026-08-28-repository-governance-stabilization -type f -print | LC_ALL=C sort
git diff --check -- specs/2026-08-28-repository-governance-stabilization
```

Because ordinary `git diff --check` does not inspect wholly untracked files,
also run a read-only direct trailing-whitespace and final-newline check over the
five files. Report the Git check and direct check separately; do not stage
intent-to-add merely to increase coverage.

Structural assertions:

1. the inventory equals the five-path allowlist exactly;
2. every file is non-empty UTF-8 text with a final newline and no trailing
   whitespace;
3. `spec.md` contains objective, canonical terms, precedence, settled
   decisions, scope/out-of-scope, Levels 0-3, fact ownership, cadence, routing,
   document gap/coverage, compatibility/migration, and stops;
4. `requirements.md` contains unique `YGS-*` identifiers and every identifier
   is represented in the acceptance matrix or a covered wildcard family;
5. `plan.md` and `tasks.md` separately identify validator RED/GREEN TDD,
   canonical-document delivery, independent review, owner acceptance, and Git
   close;
6. `validation.md` names the exact gate allowlist, contradiction negatives, and
   rung-1 ceiling.

## Contradiction Negatives

The package fails if any statement positively grants or requires:

- master control performing implementation, correction, formal review,
  validation, Git, publication, provider, deployment, pilot, production, or an
  external action;
- an internal subagent replacing a fresh visible task;
- a gate, acceptance, receipt, commit, push, or evidence result authorizing its
  successor;
- silent model/tier substitution or a model-routing savings/benchmark claim;
- `execution-state` owning transient Git facts;
- `docs/evaluation-report.md` serving as the metrics contract;
- a duplicate AgentOps universal contract, blueprint, or runbook;
- historical receipt backfill or inferred/fabricated evidence;
- automatic post-Git reconciliation without a semantic state change;
- spec acceptance being supplied by the authoring executor.

Negative review must distinguish a prohibition sentence (for example, “master
control must never validate”) from a positive duty. Keyword presence alone is
not proof of contradiction.

## Future Delivery Allowlist

At delivery preflight, applicability must be confirmed and then locked to this
exact maximum set:

```text
AGENTS.md
CHANGELOG.md
docs/operations/master-control.md
docs/operations/execution-state.md
docs/agents/executor-workflow.md
docs/operations/metrics-contract.md
docs/operations/receipt-policy.md
docs/operations/receipts/index.md
docs/adr/0001-read-only-master-control-topology.md
scripts/validate_master_control.py
tests/test_validate_master_control.py
```

If an equivalent test owner exists at the delivery fixed point,
`tests/test_validate_master_control.py` may be omitted in favor of that exact
existing path only after owner disposition; it may not be substituted silently.
All other additions, omissions of applicable owners, renames, or modifications
are scope conflicts. In particular, `docs/agents/agentops-workflow.md`, current
blueprint owners, runbook owners, and `docs/evaluation-report.md` are read-only
inputs under this spec.

## Future Delivery Positive Checks

The delivery validation contract must include:

1. public-seam unit tests for `validate(repo)`;
2. a physical CLI test for `scripts/validate_master_control.py` covering stable
   PASS/FAIL exit status and diagnostics;
3. required-owner/path and required-marker checks;
4. negative fixtures for executable master duties, transient Git fields in
   execution state, absent metrics/receipt/ADR owners, silent routing
   substitution, and evidence overclaim;
5. exact full-candidate allowlist comparison across changed, staged, and
   untracked paths;
6. `git diff --check` over the exact tracked candidate plus a direct whitespace
   check for any untracked file;
7. a no-cache/no-generated-artifact assertion after validator and test runs;
8. semantic review that local documents point to rather than reproduce the
   universal Operating Model and receipt policy;
9. an independent `FULL` review of Standards -> Spec -> Evidence -> Operations
   in a fresh visible task.

Representative future commands must be finalized against the accepted delivery
fixed point. The expected shape is:

```bash
PYTHONDONTWRITEBYTECODE=1 ./.venv/bin/python -B -m pytest tests/test_validate_master_control.py -q
PYTHONDONTWRITEBYTECODE=1 ./.venv/bin/python -B scripts/validate_master_control.py
git diff --check -- AGENTS.md CHANGELOG.md docs/operations/master-control.md docs/operations/execution-state.md docs/agents/executor-workflow.md docs/operations/metrics-contract.md docs/operations/receipt-policy.md docs/operations/receipts/index.md docs/adr/0001-read-only-master-control-topology.md scripts/validate_master_control.py tests/test_validate_master_control.py
```

No `make test-release`, broader test suite, network, provider, Graphify,
deployment, pilot, or production command is implied by this specification. A
future owner may authorize broader proportional checks separately.

## Acceptance Stops

Any unexpected RED, harness defect, drift, foreign state, extra path, missing
applicable owner, semantic contradiction, incomplete validation, or evidence
overclaim returns to owner disposition. PASS returns the candidate for owner
decision; it does not accept bytes or authorize staging, commit, push,
publication, external action, or another gate.
