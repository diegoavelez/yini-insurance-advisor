# Tasks

## Task Contract

These tasks describe future lifecycle work. They grant no action. Each
mutating, review, Git, or external task requires a fresh visible task and an
explicit fixed-point-bound owner grant. A completed task does not start its
successor.

## T00 - Owner specification decision

- Owner: human owner.
- Inputs: this exact five-file package and its Receipt Capsule v1.
- Verify: objective, canonical terms, requirements, delivery allowlist,
  validation contract, evidence ceiling, and unresolved risks.
- Output: accept, reject, or request a new bounded specification candidate.
- Optional grouping: acceptance and delivery authorization may share one owner
  decision only when both are named separately.

## T01 - Delivery preflight and applicability lock

- Executor: fresh visible delivery task.
- Route: `gpt-5.6-sol high` for initial transversal-contract classification;
  delivery implementation follows the applicable routes below.
- Verify exact fixed point, common-dir, `HEAD`, index, worktree, candidate
  inventory, allowlist applicability, and absence of truth conflict.
- Confirm the existing blueprint/runbook/evaluation owners remain read-only.
- Stop before mutation on drift, foreign state, duplicate owner, ambiguous path,
  unavailable required model, or scope expansion.
- Covers: `YGS-DLV-001`, `YGS-STP-001`.

## T02 - Validator TDD RED

- Executor: the delivery task, using `gpt-5.6-terra high` because the validator
  governs transversal repository behavior.
- Add focused tests for the importable validation seam and physical CLI.
- Add negative fixtures for all contradictions named by `YGS-DLV-004`.
- Observe expected RED against the prior contract before changing validator or
  canonical-document behavior.
- Classify invocation error or harness defect separately; neither is semantic
  RED and neither authorizes repair beyond its grant.
- Covers: `YGS-DLV-002` through `YGS-DLV-005`.

## T03 - Canonical governance document updates

- Executor: the delivery task under its documentary mutation scope.
- Update `AGENTS.md`, `docs/operations/master-control.md`,
  `docs/operations/execution-state.md`, and
  `docs/agents/executor-workflow.md`.
- Encode read-only topology, visible tasks, compact cadence, routing, fact
  ownership, semantic-only execution state, evidence ceiling, and stops.
- Preserve only semantic evidence and dated historical external observations;
  remove transient Git ownership from execution state.
- Covers: `YGS-CTL-*`, `YGS-AUT-*`, `YGS-SDD-*`, `YGS-RTE-*`, `YGS-FCT-*`.

## T04 - Missing local contracts and durable decision

- Executor: the delivery task under its documentary mutation scope.
- Add `docs/operations/metrics-contract.md` as the semantic contract for metric
  definitions, owners, inputs, limitations, and change control.
- Add `docs/operations/receipt-policy.md` as a local projection that points to,
  and does not copy, the universal policy.
- Add `docs/operations/receipts/index.md` empty of historical backfill and ready
  for prospective append-only entries.
- Add `docs/adr/0001-read-only-master-control-topology.md` using the repository
  ADR format and recording the settled trade-off.
- Update `CHANGELOG.md` only after the complete candidate is assembled.
- Covers: `YGS-DOC-*`, `YGS-DLV-006`, `YGS-EVD-003`.

## T05 - Validator GREEN and local delivery verification

- Executor: the delivery task; deterministic mechanisms first.
- Update `scripts/validate_master_control.py` minimally to satisfy the RED tests.
- Run focused tests, physical CLI validation, exact allowlist checks,
  contradiction negatives, cache/artifact checks, and `git diff --check`.
- Correct only within an explicitly granted delivery correction budget; stop on
  harness defect, drift, or unexpected failure.
- Return a Receipt Capsule capped at rung 2.
- Covers: `YGS-DLV-*`, `YGS-EVD-002`, `YGS-STP-001`.

## T06 - Independent FULL review

- Executor: fresh visible review task, never the delivery author.
- Route: `gpt-5.6-sol high`.
- Bind to the exact candidate fingerprint and review all allowlisted paths in
  Standards -> Spec -> Evidence -> Operations order.
- Check requirement traceability, negative contradictions, validator integrity,
  canonical-owner coherence, migration safety, and evidence wording.
- Return findings and `PRESENT_FOR_OWNER_DECISION` only on classified PASS. Do
  not correct or accept bytes.
- Covers: `YGS-AUT-004`, `YGS-REV-001`.

## T07 - Correction, only if owner-authorized

- Executor: fresh visible correction task.
- Route: `gpt-5.6-terra medium`, elevated to `high` for transversal findings;
  P0/P1 or material ambiguity returns first to `gpt-5.6-sol high` owner-facing
  disposition.
- Bind the correction to explicit findings, fixed point, allowlist, validation,
  and cycle budget. Use `NARROW_DELTA` only when the universal convergence
  contract permits it; otherwise require `FULL` review.
- No silent retry, harness repair, or scope expansion.

## T08 - Owner final acceptance and close

- Owner: human owner.
- Inputs: complete candidate, delivery receipt, independent review receipt, and
  any authorized correction/re-review receipts.
- Decide acceptance separately from each potential Git grant.
- If Git actions are desired, name exact staging, commit, and push grants with
  their own preconditions, fixed point, path scope, and terminal evidence.
- Leave provider execution, deployment, pilot, production, and successor work
  closed.
- Covers: `YGS-AUT-005` through `YGS-AUT-007`, `YGS-CLS-001`.

## Task Completion Rule

No task is complete without its declared exact paths, observed commands and
results, skipped checks, evidence ceiling, residual risks, Git state, and next
owner decision. No task may accept its own bytes.
