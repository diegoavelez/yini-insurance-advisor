# Plan

## Objective

Deliver the smallest complete repository-local governance stabilization that
satisfies `requirements.md`, updates all applicable canonical owners, and
returns one candidate for independent review without copying the universal
AgentOps contract.

## Expected Delivery Allowlist

The delivery executor must revalidate applicability at its exact fixed point
and remain within the allowlist declared in `spec.md`. The current expected
candidate includes the five existing governance/change-log paths, three new
local contract/index paths, one new ADR, the validator, and its public-seam
test. `docs/agents/agentops-workflow.md`, blueprint owners, runbook owners, and
historical evaluation evidence are read-only inputs unless the owner issues a
new fixed-point-bound scope decision.

## Assumptions

- The owner accepts the settled decisions in this package without reopening
  the universal Operating Model.
- No equivalent metrics contract, receipt policy/index, ADR, or validator test
  owner appears before delivery preflight.
- Existing accepted semantic evidence can be retained without preserving
  transient Git snapshots.
- The validator can remain deterministic, local, network-free, and read-only.

## Risks and Controls

- **Universal-contract duplication:** local documents define only Yini choices,
  pointers, schema projections, and stricter local rules.
- **Truth loss during execution-state migration:** retain semantic evidence,
  risks, blockers, and next decision; remove only transient Git ownership.
- **Validator self-fulfillment:** establish RED fixtures and public CLI behavior
  before changing implementation, then run independent review.
- **Overbroad allowlist:** stop on every unlisted path or newly discovered owner
  conflict; do not opportunistically reconcile adjacent documentation.
- **Ceremonial overhead:** apply the compact Level 0 rule and grouped decision
  opportunities exactly, while preserving distinct grants.
- **Routing failure:** return unavailable, inadequate, or ambiguous route
  selection to the owner; never substitute silently.

## Delivery Sequence

### Phase 0 - Owner spec decision

1. Review this five-file package at fixed point
   `b1f1e49f6aab0672e7d34e7b3fabbf5629e82c0a` plus its exact untracked-byte
   hashes.
2. Accept or reject the spec candidate.
3. If accepted, optionally combine spec acceptance with a separately named
   delivery grant bound to a fresh visible task, exact fixed point, allowlist,
   validators, stops, and evidence ceiling.

### Phase 1 - Delivery preflight and scope binding

1. In the delivery task, verify physical worktree, Git common-dir, exact `HEAD`,
   index, worktree, and complete candidate inventory before mutation.
2. Reconcile the logical owners against the exact allowlist. Stop if a new
   equivalent owner, drift, or conflict changes applicability.
3. Record the expected RED/GREEN validator commands and artifact-free
   environment before executing them.

### Phase 2 - Validator TDD RED

1. Add tests at the importable `validate(repo)` seam for every required marker,
   forbidden contradiction, path owner, and execution-state transient-field
   rejection.
2. Add a physical CLI test for pass/fail exit status and stable output.
3. Run only the focused validator tests and preserve the expected RED evidence.
4. Stop on harness defect; do not classify a broken test as candidate RED.

### Phase 3 - Canonical documentary delivery

1. Rewrite the master-control projection as a strict read-only tower.
2. Migrate execution state to semantic-only ownership without fabricating or
   deleting meaningful historical evidence.
3. Update executor workflow for fresh visible tasks, bounded subagent support,
   compact cadence, routing returns, and complete receipts.
4. Update `AGENTS.md` only with the compact always-read local kernel needed to
   point at these owners.
5. Add the metrics contract, receipt policy projection/index, and read-only
   topology ADR.
6. Update `CHANGELOG.md` for the complete candidate.

### Phase 4 - Validator TDD GREEN

1. Make the smallest validator change that enforces the accepted new contract.
2. Run focused tests until the candidate reaches GREEN within the authorized
   correction budget.
3. Run the validator through its physical CLI with bytecode/cache creation
   disabled.
4. Verify exact candidate allowlist and whitespace integrity.

### Phase 5 - Delivery return

1. Return the complete candidate, hashes, focused test results, known skips,
   evidence ceiling, risks, and next gate.
2. Do not self-review formally, accept, stage, commit, push, publish, or begin a
   successor gate.

### Phase 6 - Independent full review

1. Use a fresh visible task routed to `gpt-5.6-sol` at reasoning `high`.
2. Bind review to the exact complete delivery candidate and review Standards ->
   Spec -> Evidence -> Operations.
3. Evaluate all allowlisted files, including canonical documents, new local
   contracts, ADR, validator, tests, and changelog.
4. Return findings for correction or owner disposition; do not mutate bytes.

### Phase 7 - Owner close and optional Git grants

1. The owner accepts, rejects, or requests correction of the reviewed
   candidate.
2. If accepted, the owner may bundle separately named grants for exact staging,
   commit, and push, each with its own preconditions and terminal receipt.
3. Provider, deployment, pilot, production, and any semantic successor remain
   separate later decisions.
4. Do not run automatic post-Git reconciliation unless semantic state changed.

## Verification Strategy

- Structural: exact path inventory, required headings, requirement-ID coverage,
  and cross-reference integrity.
- Behavioral: validator import seam and physical CLI RED/GREEN tests.
- Negative: fixtures for master execution duties, transient Git facts, missing
  local owners, silent model substitution, duplicate owner creation, and
  evidence overclaim.
- Documentary: contradiction review across every canonical owner and the
  universal-to-local seam.
- Scope: compare all changed, staged, untracked, ignored-relevant, and generated
  paths with the accepted allowlist.
- Evidence: cap the delivery at rung 2 and state every external or human check
  not performed.
