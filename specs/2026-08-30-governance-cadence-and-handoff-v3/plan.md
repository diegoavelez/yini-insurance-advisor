# Plan

## Objective

Deliver the smallest complete repository-local change that enforces the
accepted owner-interruption budget, grouped-decision semantics, contingency
boundaries, and selective CompactHandoff v3 policy without weakening the
strictly read-only master topology or copying the universal plugin contract.

## Affected Files

Specification gate, exactly five new files:

- `spec.md`
- `requirements.md`
- `plan.md`
- `tasks.md`
- `validation.md`

Future delivery mutation allowlist, exactly eight paths:

- `CHANGELOG.md`
- `docs/operations/master-control.md`
- `docs/operations/execution-state.md`
- `docs/agents/executor-workflow.md`
- `docs/agents/agentops-workflow.md`
- `docs/adr/0002-owner-interruption-budget-and-compacthandoff-v3.md`
- `scripts/validate_master_control.py`
- `tests/test_validate_master_control.py`

The accepted five spec paths are immutable governed inputs in delivery and are
included in the complete thirteen-path review candidate.

## Assumptions

- The installed plugin continues to expose the accepted `0.11.x` CompactHandoff
  v3 contract when delivery starts.
- The repository retains AgentOps policy `1.4`, profile `provider-eval`, and the
  current manual Yini routing directive.
- `docs/adr/0002-*.md` remains the next available ADR slot at delivery
  preflight.
- The current master-control validator remains the correct deterministic seam
  for repository-local governance contradictions.
- No new canonical owner or conflicting accepted spec appears before delivery.

## Risks and Controls

- **Gate-count rigidity:** define normal budgets plus explicit promotion and
  contingency rules; never suppress a real owner decision to satisfy a number.
- **Authority collapse:** every grouped decision retains named grants, task
  identities, preconditions, scope, consumption, stops, and receipts.
- **Master-control expansion:** administrative dispatch is limited to tasks
  already named by an existing grant and performs no lifecycle action itself.
- **V3 ceremony:** require v3 only where candidate or worktree binding reduces
  ambiguity; keep Level 0 and routine Level 1/Git handoffs plain.
- **V3 trust overclaim:** validate that transport equality never becomes grant,
  manifest-truth, Git, acceptance, or receipt evidence.
- **Plugin duplication:** update only a concise adapter pointer and minimum
  version; never copy implementation or schema bytes.
- **Validator self-fulfillment:** establish independent negative fixtures and a
  meaningful RED before canonical or validator implementation changes.
- **Recursive closeout:** update canonical documents inside delivery and permit
  no automatic second administrative lifecycle without semantic change.
- **Historical rewriting:** leave the accepted governance spec, ADR 0001, and
  publication receipts unchanged.

## Delivery Sequence

### Phase 0 - Specification decision

1. Present this exact five-file package and its hashes at fixed point
   `c603647d280049f8bb8a2afc0678e7065341fade`.
2. The owner accepts, rejects, or requests a bounded spec correction.
3. If accepted, the same owner decision may separately name the delivery grant
   and any exact primary-plus-dormant-retry bundle.
4. No delivery task starts from spec creation alone.

### Phase 1 - Delivery preflight

1. Use a fresh visible delivery task and verify physical root, Git common-dir,
   exact `HEAD`, index, worktree, ignored/generated inputs, and complete
   five-path accepted-spec inventory.
2. Confirm the eight-path mutation allowlist remains applicable and ADR 0002 is
   available.
3. Verify installed plugin version and the authoritative v3 reference without
   modifying or copying plugin resources.
4. Record exact validators, cache-safe runtime, stop conditions, model route,
   and candidate fingerprint before mutation.

### Phase 2 - Validator TDD RED

1. Add focused tests for gate-budget definitions and exact counts.
2. Add negative fixtures for task/gate conflation, measured-efficiency claims,
   excess retries, automatic harness repair/resume, generic retry authority,
   v3 authority overclaim, missing v3 boundary selection, fallback, obsolete
   minimum version, and unconditional second administrative closeout.
3. Exercise both `validate(repo)` and the physical CLI.
4. Observe a meaningful expected RED against the prior canonical contract.
5. Stop on invocation error, harness defect, or unexpected RED; do not treat it
   as candidate behavior.

### Phase 3 - Canonical documentary delivery

1. Add canonical terminology and the SDD owner-interruption matrix to master
   control.
2. Add executor-facing grouped-decision, dispatch, retry/harness, and v3
   selection rules to executor workflow.
3. Raise the compact adapter minimum to `0.11.0` and add only the concise local
   selection pointer needed by Yini.
4. Update execution state with the current semantic work, evidence ceiling,
   risks, blockers, and next owner decision without transient Git facts.
5. Add ADR 0002 recording the budget/selective-v3 trade-off.
6. Update the changelog after the complete candidate is assembled.

### Phase 4 - Validator TDD GREEN

1. Implement the smallest deterministic validator changes needed by the RED
   fixtures.
2. Run focused tests and physical CLI until GREEN within the authorized
   correction budget.
3. Validate exact path inventory, UTF-8/final-newline/trailing-whitespace
   integrity, no cache/generated artifacts, and no staged delta.
4. Report all skipped broader checks and cap evidence at rung 2.

### Phase 5 - Delivery return

1. Return one complete thirteen-path candidate fingerprint, exact changed
   paths, commands/results, evidence ceiling, risks, and Receipt Capsule v1.
2. Produce a CompactHandoff v3 artifact for the required delivery-to-review
   boundary in the OS temporary directory.
3. Do not self-review formally, accept, correct review findings, stage, commit,
   push, publish, or begin another gate.

### Phase 6 - Independent FULL review

1. Use a fresh visible task routed to `gpt-5.6-sol` at reasoning `high`.
2. Independently observe the complete candidate manifest and verify the v3
   handoff without treating it as authority or Git truth.
3. Review Standards -> Spec -> Evidence -> Operations against the accepted
   package and all thirteen candidate paths.
4. Return classified findings or `PRESENT_FOR_OWNER_DECISION` without mutation
   or acceptance.

### Phase 7 - Optional correction and re-review

1. The owner disposes exact findings before correction.
2. One decision may separately name a fresh bounded correction task and a
   conditional fresh `NARROW_DELTA` task when convergence rules permit it.
3. Transfer only the corrected candidate delta through CompactHandoff v3.
4. P0/P1, trust-boundary change, exhausted semantic cycles, drift, harness
   defect, validation gap, or ambiguity returns to owner disposition.

### Phase 8 - Final acceptance and optional close bundle

1. Present the complete reviewed candidate and all delivery/review receipts.
2. The owner accepts, rejects, or requests a permitted correction.
3. One exact owner decision may separately name any required semantic freeze,
   differential review, staging, commit, and push grants with ordered
   preconditions and fresh task identities.
4. Do not run a second administrative closeout merely because Git completed.
5. Provider, deployment, pilot, production, Graphify, and successor product
   work remain closed.

## Verification Strategy

- **Structural:** exact five-path spec inventory, eight-path mutation allowlist,
  thirteen-path review candidate, headings, unique requirement IDs, and
  cross-file references.
- **Behavioral:** focused RED/GREEN tests through the importable validator seam
  and physical CLI.
- **Negative:** gate/task conflation, wrong counts, hidden contingencies, excess
  retries, generic repair, v3 fallback/authority overclaim, obsolete plugin
  minimum, and recursive closeout.
- **Documentary:** compare master control, executor workflow, adapter, execution
  state, ADR, changelog, spec, and universal pointers for contradiction.
- **Handoff:** issue v3 with a closed candidate manifest, independently observe
  the review manifest, verify equality, and preserve the transport-only ceiling.
- **Scope:** compare changed, staged, untracked, ignored-relevant, and generated
  state against the accepted partitions.
- **Evidence:** rung 1 for this spec; at most rung 2 for future local delivery.

## Definition of Done

- Every `YCH-*` requirement is traced to implementation and validation.
- The complete candidate stays inside the accepted scope.
- Focused tests, physical CLI, whitespace, inventory, and artifact checks pass.
- Independent `FULL` review completes and the owner decides the exact bytes.
- No unreported finding, skipped check, evidence overclaim, secret, or successor
  authority remains hidden.

## Unresolved Decisions

None for specification synthesis. Delivery applicability, exact task IDs,
candidate hashes, commands, and Git grants must be fixed at their later gates.
