# Tasks

## Task Contract

These tasks describe future lifecycle work and grant no action. Every delivery,
correction, independent review, validation, Git, provider, deployment, pilot,
production, or external action requires the applicable owner authority and a
fresh visible task. Administrative dispatch may create only tasks already
named inside an exact unconsumed grant.

## T00 - Owner specification decision

- Owner: human owner.
- Inputs: exact five-file package, fixed point, hashes, validation results, and
  Receipt Capsule v1.
- Decide: accept, reject, or request a bounded spec correction.
- Optional grouping: acceptance may share the decision with a separately named
  delivery grant and exact primary-plus-dormant-retry bundle.
- Covers: `YCH-EVD-001`, `YCH-STP-*`.

## T01 - Delivery preflight and scope lock

- Executor: fresh visible delivery task.
- Route: `gpt-5.6-sol high` for the initial transversal-contract and ambiguity
  assessment; TDD implementation follows the Terra route below.
- Verify root, common-dir, `HEAD`, index, worktree, complete candidate
  partitions, five accepted spec hashes, plugin version/reference, runtime,
  ADR slot, and eight-path mutation allowlist.
- Stop before mutation on any mismatch, unknown state, unavailable required
  route, or scope expansion.
- Covers: `YCH-DLV-001`, `YCH-HND-009`, `YCH-STP-001`.

## T02 - Validator TDD RED

- Executor: delivery task using `gpt-5.6-terra high` because the validator
  governs a transversal authority contract.
- Add independent positive and negative fixtures for all `YCH-VAL-*` and
  applicable `YCH-BUD-*`, `YCH-AUT-*`, `YCH-RET-*`, and `YCH-HND-*` rules.
- Exercise `validate(repo)` and the physical CLI.
- Preserve the meaningful expected RED before changing canonical documents or
  validator behavior.
- Stop on invocation error, harness defect, or unexpected RED.

## T03 - Canonical cadence and handoff delivery

- Executor: delivery task under its eight-path mutation allowlist.
- Update master control with canonical terms, normal budgets, grouped decisions,
  administrative dispatch, and contingency returns.
- Update executor workflow with exact bundles, retry/harness rules, and the v3
  selection matrix.
- Raise adapter minimum to `0.11.0` and preserve its pointer-based role.
- Update execution state semantically without transient Git facts.
- Add ADR 0002 and update changelog before returning the candidate.
- Covers: `YCH-TERM-*`, `YCH-BUD-*`, `YCH-AUT-*`, `YCH-RET-*`,
  `YCH-HND-*`, `YCH-DLV-002`, `YCH-DLV-003`.

## T04 - Validator GREEN and local verification

- Executor: delivery task; deterministic mechanisms first.
- Update the validator minimally to satisfy the accepted tests.
- Run the focused suite, physical CLI, exact inventory, whitespace, no-cache,
  and no-generated-artifact checks.
- Keep accepted specs byte-identical and return one thirteen-path candidate.
- Produce Receipt Capsule v1 capped at rung 2.
- Covers: `YCH-DLV-004` through `YCH-DLV-007`, `YCH-VAL-*`,
  `YCH-EVD-002`, `YCH-EVD-003`.

## T05 - Required CompactHandoff v3 review transfer

- Executor: delivery task at its terminal return.
- Issue a `handoff.v3` artifact with closed candidate manifest and transport
  metadata under the OS temporary directory.
- Include work-unit type, SDD depth, fixed point, scope/exclusions, sources,
  failures/contradictions, ordered acceptance criteria, validators, stops,
  evidence ceiling, suggested skills, redactions, absent evidence, and next
  gate.
- Do not treat issue success as manifest truth, authority, acceptance, or
  independent observation.
- Covers: `YCH-HND-003`, `YCH-HND-005` through `YCH-HND-008`.

## T06 - Independent FULL review

- Executor: fresh visible review task, never the delivery author.
- Route: `gpt-5.6-sol high`.
- Independently observe the candidate manifest, verify v3 transport, and review
  Standards -> Spec -> Evidence -> Operations.
- Return findings or `PRESENT_FOR_OWNER_DECISION`; do not mutate or accept.
- Covers: `YCH-REV-001`, `YCH-STP-*`.

## T07 - Owner finding disposition and optional correction bundle

- Owner: human owner.
- If findings exist, accept no bytes until they are explicitly disposed.
- One decision may name a fresh correction grant plus a conditional fresh
  `NARROW_DELTA` grant when fixed points, paths, findings, validators, task
  identities, and convergence limits are exact.
- Transfer any corrected candidate through a v3 delta handoff.
- A harness defect remains a separately scoped repair decision and owner
  disposition afterward.
- Covers: `YCH-AUT-002`, `YCH-RET-004`, `YCH-HND-004`, `YCH-REV-002`.

## T08 - Owner final acceptance and optional close bundle

- Owner: human owner.
- Inputs: exact candidate, delivery receipt, `FULL` receipt, and any authorized
  correction/re-review receipts.
- Decide acceptance separately from each named freeze, differential-review,
  staging, commit, and push grant, even when grouped in one decision.
- Require each fresh task to observe its preconditions and return its terminal
  receipt before the next conditional grant becomes eligible.
- Do not open a second administrative closeout without semantic change.
- Covers: `YCH-AUT-003`, `YCH-CLS-001`, `YCH-STP-002`.

## T09 - External rungs, only if later authorized

- Provider execution, deployment, pilot, production, human/usability, and other
  external rungs remain separate future decisions and tasks.
- CompactHandoff may transport context but grants no external authority.
- No external task is authorized by this package.
- Covers: `YCH-BUD-004`, `YCH-HND-007`, `YCH-EVD-002`.

## Task Completion Rule

Every task returns its identity, fixed point, exact changed/staged delta,
commands and results, skipped checks, classified failures, evidence ceiling,
residual risks, Receipt Capsule v1, and next owner decision. No task accepts its
own bytes or auto-starts a successor.
