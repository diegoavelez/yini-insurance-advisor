# Requirements

## Status

These requirements belong to `YINI-GOVERNANCE-STABILIZATION` and are a Level 2
candidate under `YINI-GOVERNANCE-STABILIZATION-SPEC-1`. They are not accepted
until the owner decides the spec gate.

## Verifiable Requirements

### Control topology

- **YGS-CTL-001:** `docs/operations/master-control.md` SHALL define master
  control as strictly read-only and limit it to orientation, classification,
  visible-task/handoff preparation, receipt intake, and decision proposals.
- **YGS-CTL-002:** The repository governance contract SHALL forbid master
  control from implementation, correction, formal or independent review,
  validation, Git, publication, provider execution, deployment, pilot,
  production, and external actions.
- **YGS-CTL-003:** Implementation, correction, independent review, Git, and
  external actions SHALL each use a fresh visible task with an explicit bounded
  grant.
- **YGS-CTL-004:** An internal subagent SHALL NOT satisfy a visible-task
  boundary and MAY support work only when there are at least two independent,
  bounded, non-mutating analysis workstreams.

### Authority and cadence

- **YGS-AUT-001:** Every gate, task, acceptance, review result, commit, push,
  and receipt SHALL be non-authorizing unless accompanied by an explicit owner
  grant for the named action, task, fixed point, and scope.
- **YGS-AUT-002:** Spec acceptance and delivery authorization MAY be decided
  together only when separately named in the owner decision.
- **YGS-AUT-003:** Delivery SHALL update all applicable canonical documents
  before returning a complete candidate.
- **YGS-AUT-004:** Independent review SHALL occur in a fresh visible task and
  cover the complete candidate, including canonical documents.
- **YGS-AUT-005:** Final acceptance MAY be decided together with separately
  named staging, commit, and push grants; each Git action SHALL retain separate
  preconditions, consumption, evidence, and terminal status.
- **YGS-AUT-006:** Provider execution, deployment, pilot, and production SHALL
  remain separate gates and visible tasks.
- **YGS-AUT-007:** A Git action SHALL NOT trigger automatic documentary
  reconciliation unless semantic state changes.
- **YGS-AUT-008:** Level 0 work SHOULD use proportional delivery/review and
  close without creating unnecessary lifecycle tasks.

### SDD and routing

- **YGS-SDD-001:** The local contract SHALL define Levels 0 through 3 and SHALL
  require the five-file package for Level 2 work.
- **YGS-RTE-001:** Validated deterministic mechanics SHALL use a validated
  mechanism and no model when one exists.
- **YGS-RTE-002:** Level 0 and mechanical documentation SHALL route to
  `gpt-5.6-luna` at reasoning `max`.
- **YGS-RTE-003:** TDD implementation, correction, and `NARROW_DELTA` review
  SHALL route to `gpt-5.6-terra` at reasoning `medium`, elevated to `high` for
  transversal risk.
- **YGS-RTE-004:** Master orientation, architecture, public contracts, trust
  boundaries, `FULL` review, P0/P1, and material ambiguity SHALL route to
  `gpt-5.6-sol` at reasoning `high`.
- **YGS-RTE-005:** Sol/Terra `xhigh` or `max` SHALL require representative
  evidence or exceptional owner authorization.
- **YGS-RTE-006:** Ambiguous classification or an unavailable/inadequate route
  SHALL return to the owner without silent substitution.
- **YGS-RTE-007:** Routing documentation SHALL state that the directive is
  manual, Yini-specific, revocable, non-benchmark, non-reusable as evidence,
  not a savings claim, and non-authorizing.

### Fact and document ownership

- **YGS-FCT-001:** Git SHALL exclusively own live branch, `HEAD`, index,
  worktree, refs, remotes, divergence, and tracking facts.
- **YGS-FCT-002:** `docs/operations/execution-state.md` SHALL own semantic work
  state, accepted evidence ceiling, risks, blockers, and the next owner
  decision, and SHALL NOT copy transient Git facts.
- **YGS-FCT-003:** Live external facts SHALL remain owned by the external
  system; documentary observations SHALL be dated historical evidence only.
- **YGS-DOC-001:** `PRD.md`, `docs/architecture.md`, and `specs/tech-stack.md`
  SHALL remain the current blueprint owners; no duplicate blueprint SHALL be
  created.
- **YGS-DOC-002:** `docs/mvp-go-live.md` and
  `docs/category-onboarding-playbook.md` SHALL remain runbook owners; no
  duplicate runbook SHALL be created.
- **YGS-DOC-003:** `docs/evaluation-report.md` SHALL be classified as
  historical evidence, not the metrics contract.
- **YGS-DOC-004:** `docs/agents/agentops-workflow.md` SHALL remain a compact
  adapter and SHALL NOT duplicate the universal plugin contract.
- **YGS-DOC-005:** Delivery SHALL add a local metrics contract defining metric
  semantics, ownership, evidence inputs, claim limits, and change control.
- **YGS-DOC-006:** Delivery SHALL add a local receipt policy projection and an
  append-only receipt index without backfilling historical receipts or copying
  the universal receipt policy.
- **YGS-DOC-007:** Delivery SHALL add an ADR for the read-only master-control
  topology using the repository's first `docs/adr/0001-*.md` slot.

### Delivery and validation

- **YGS-DLV-001:** The delivery candidate SHALL contain only applicable paths
  from the exact allowlist in `spec.md`; any extra path or omitted applicable
  path SHALL stop for owner disposition.
- **YGS-DLV-002:** `scripts/validate_master_control.py` SHALL be changed through
  TDD at its public CLI and importable validation seam.
- **YGS-DLV-003:** Validator tests SHALL first demonstrate RED against the
  accepted old contract, then GREEN against the complete new candidate.
- **YGS-DLV-004:** The validator SHALL reject executable master duties,
  transient Git facts in execution state, missing receipt/metrics/ADR owners,
  silent model substitution, and any required-contract omission.
- **YGS-DLV-005:** The validator SHALL preserve a deterministic, read-only,
  network-free execution path and SHALL create no cache or repository artifact.
- **YGS-DLV-006:** `CHANGELOG.md` and every applicable canonical governance
  document SHALL be updated inside delivery before review.
- **YGS-REV-001:** Independent review SHALL use Standards -> Spec -> Evidence ->
  Operations order and classify findings without correcting the candidate.
- **YGS-CLS-001:** Owner acceptance, Git actions, provider actions, and later
  lifecycle gates SHALL remain outside the delivery and review tasks unless
  separately and explicitly granted.

### Evidence and stops

- **YGS-EVD-001:** Specification-only checks SHALL claim at most evidence rung
  1 (static/schema).
- **YGS-EVD-002:** A future delivery MAY claim at most rung 2 after its local
  deterministic tests pass; it SHALL NOT claim integration, controlled
  synthetic, provider, human/usability, pilot, or production evidence.
- **YGS-EVD-003:** No historical receipt SHALL be backfilled and no missing
  evidence SHALL be inferred or fabricated.
- **YGS-STP-001:** Drift, foreign state, truth conflict, material ambiguity,
  sensitive-data risk, scope expansion, harness defect, unavailable required
  route, or incomplete evidence SHALL stop fail-closed without silent repair,
  cleanup, retry, substitution, or gate advancement.

## Acceptance Matrix

| Concern | Requirement IDs | Primary proof |
|---|---|---|
| read-only topology | `YGS-CTL-*`, `YGS-AUT-*` | canonical-document assertions and contradiction negatives |
| SDD and routing | `YGS-SDD-*`, `YGS-RTE-*` | exact routing table and stop-path tests |
| fact ownership | `YGS-FCT-*` | execution-state schema tests and forbidden transient-field fixtures |
| document ownership | `YGS-DOC-*` | required-path/marker tests and duplicate-owner negatives |
| delivery mechanics | `YGS-DLV-*` | RED/GREEN validator tests plus exact allowlist inventory |
| independent review and close | `YGS-REV-*`, `YGS-CLS-*` | fresh-task review receipt and owner decision |
| evidence discipline | `YGS-EVD-*`, `YGS-STP-*` | Receipt Capsule, evidence ceiling, and negative fixtures |
