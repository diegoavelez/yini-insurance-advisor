# Requirements

## Status

These requirements belong to `YINI-GOVERNANCE-CADENCE-AND-HANDOFF-V3` and are
a Level 2 candidate under
`YINI-GOVERNANCE-CADENCE-AND-HANDOFF-V3-SPEC-1`. They are not accepted until
the owner decides the specification gate.

## Verifiable Requirements

### Canonical language

- **YCH-TERM-001:** The local governance contract SHALL distinguish an owner
  approval gate from an executor task.
- **YCH-TERM-002:** The contract SHALL define normal gate budget, contingency
  gate, lifecycle bundle, administrative dispatch, CompactHandoff v3, and plain
  compact handoff without treating any of them as authority.
- **YCH-TERM-003:** Gate counts SHALL count owner decisions only and SHALL NOT
  be presented as executor-task counts or measured efficiency evidence.

### SDD gate budget

- **YCH-BUD-001:** Level 0 SHALL normally require two owner approval gates:
  bounded delivery/validation and final acceptance with optional exact Git
  grants.
- **YCH-BUD-002:** Level 1 or Level 2 with an accepted applicable spec SHALL
  normally require three owner approval gates: spec acceptance plus delivery,
  independent review, and final acceptance plus optional close/Git grants.
- **YCH-BUD-003:** Level 1 or Level 2 without the required spec SHALL add one
  specification-candidate gate, producing a normal total of four.
- **YCH-BUD-004:** Level 3 SHALL retain the applicable Level 2 core and SHALL
  add separate decisions for each required provider, deployment, pilot,
  production, or evidence-dependent external rung.
- **YCH-BUD-005:** Findings, drift, harness defects, validation gaps, unavailable
  routes, scope changes, and other stop conditions SHALL be reported as
  contingency gates instead of being hidden inside the normal budget.
- **YCH-BUD-006:** The budget SHALL be a governance target and SHALL NOT claim
  measured token, latency, cost, quality, or productivity improvement.

### Bundles, dispatch, and authority

- **YCH-AUT-001:** Separately named spec-acceptance and delivery grants MAY
  share one owner decision.
- **YCH-AUT-002:** After owner disposition of exact findings, a bounded
  correction grant and a conditional fresh review grant MAY share one owner
  decision while retaining separate task identities, fixed-point
  preconditions, scopes, stops, and receipts.
- **YCH-AUT-003:** Final acceptance MAY share one owner decision with separately
  named exact canonical-freeze, differential-review, staging, commit, and push
  grants; every step SHALL retain its own eligibility and terminal result.
- **YCH-AUT-004:** Master control MAY administratively create and dispatch only
  the fresh tasks already named inside an applicable unconsumed grant without
  requesting duplicate approval for task creation.
- **YCH-AUT-005:** Administrative dispatch SHALL NOT permit master control to
  implement, correct, formally review, validate, accept, mutate Git, access a
  provider, deploy, pilot, produce, or perform another external action.
- **YCH-AUT-006:** Any unnamed task, changed fixed point, failed intermediate
  precondition, new semantic decision, or scope expansion SHALL return to the
  owner instead of consuming successor authority.
- **YCH-AUT-007:** Grouped grants SHALL NOT merge actions, weaken fresh-task
  topology, or authorize cleanup, repair, retry, external evidence, or a later
  semantic work unit unless separately named.

### Retry and harness contingencies

- **YCH-RET-001:** A mechanical retry bundle SHALL contain exactly one primary
  invocation grant and one dormant retry grant with distinct predeclared task
  identities and identical complete execution-context identity.
- **YCH-RET-002:** The dormant retry SHALL be eligible only for the declared
  invocation-error class before target mutation and after unchanged context is
  proven by evidence and retry preflight.
- **YCH-RET-003:** A second retry, third attempt, alternate invocation, target
  mutation, unknown state, Git, provider/network activity, external action, or
  destructive action SHALL be retry-ineligible.
- **YCH-RET-004:** A harness defect SHALL be distinct from a candidate finding
  and mechanical retry and SHALL request a separately scoped repair decision
  plus owner disposition afterward.
- **YCH-RET-005:** Generic authorization language such as “retry if needed” or
  “repair the harness if needed” SHALL NOT satisfy the local exact-grant
  contract.

### CompactHandoff selection and trust

- **YCH-HND-001:** Level 0 and deterministic same-checkout Git mechanics SHALL
  use a plain compact handoff unless a separately identified material boundary
  promotes the selection.
- **YCH-HND-002:** Level 1 SHALL use CompactHandoff v3 when crossing a worktree,
  candidate-bound retry, long-context, or exact candidate boundary and MAY use
  a plain compact handoff otherwise.
- **YCH-HND-003:** Level 2 and Level 3 delivery-to-independent-review boundaries
  SHALL use CompactHandoff v3.
- **YCH-HND-004:** Level 2 and Level 3 correction-to-`NARROW_DELTA` or renewed
  `FULL` boundaries SHALL use a v3 delta handoff.
- **YCH-HND-005:** New Yini issuance SHALL use `handoff.v3`; a required v3
  boundary SHALL stop without fallback on unavailable issue/verify, version
  mismatch, manifest ambiguity, or verification failure.
- **YCH-HND-006:** `local-pointer` SHALL be the default and `portable-inline`
  SHALL require explicit selection; generated artifacts SHALL remain outside
  the repository unless separately authorized.
- **YCH-HND-007:** V3 SHALL NOT be described as authenticating authority,
  observing Git or manifest truth, consuming a grant, preventing replay,
  accepting bytes, or replacing independent preflight or Receipt Capsule v1.
- **YCH-HND-008:** The repository SHALL point to the installed handoff skill and
  v3 reference and SHALL NOT copy plugin code, schemas, references, fixtures,
  or skills or create a local wrapper around plugin internals.
- **YCH-HND-009:** The repository adapter SHALL raise
  `plugin_minimum_version` to `0.11.0` while preserving policy `1.4` and profile
  `provider-eval`.

### Delivery and durable decision

- **YCH-DLV-001:** Delivery SHALL modify only the eight-path mutation allowlist
  in `spec.md`; the complete review candidate SHALL also contain the five
  accepted spec paths unchanged.
- **YCH-DLV-002:** Delivery SHALL update every applicable canonical document,
  the new ADR, and `CHANGELOG.md` before returning the complete candidate for
  independent review.
- **YCH-DLV-003:** The new ADR SHALL record why fewer owner interruptions are
  compatible with separate authorities and why v3 is selective rather than
  universal.
- **YCH-DLV-004:** `scripts/validate_master_control.py` SHALL be updated through
  TDD at its importable validation seam and physical CLI.
- **YCH-DLV-005:** Validator tests SHALL demonstrate meaningful RED against the
  prior local contract before the validator or canonical documents are changed.
- **YCH-DLV-006:** Delivery validation SHALL be local, deterministic,
  network-free, provider-free, bytecode/cache-safe, and capped at evidence rung
  2.
- **YCH-DLV-007:** `AGENTS.md`, historical specs/receipts, plugin files, product
  code, data, dependencies, runtime, and deployment configuration SHALL remain
  unchanged.

### Validation, review, and close

- **YCH-VAL-001:** The validator SHALL reject missing or contradictory gate
  budgets, treating tasks as owner gates, or presenting the budget as measured
  efficiency evidence.
- **YCH-VAL-002:** The validator SHALL reject more than one dormant mechanical
  retry, automatic harness repair/resume, or generic retry/repair authority.
- **YCH-VAL-003:** The validator SHALL reject treating CompactHandoff as
  authority, silent fallback from a required v3 boundary, missing required v3
  selection, or an adapter minimum below `0.11.0`.
- **YCH-VAL-004:** The validator SHALL reject a mandatory second administrative
  closeout or automatic post-Git reconciliation when no semantic state changed.
- **YCH-REV-001:** A fresh independent `FULL` review SHALL examine the complete
  candidate in Standards -> Spec -> Evidence -> Operations order without
  correcting or accepting it.
- **YCH-REV-002:** Only an applicable owner decision SHALL authorize correction,
  a conditional fresh re-review, final acceptance, canonical freeze, Git, or
  another lifecycle phase.
- **YCH-CLS-001:** A clean close SHALL consume only the normal applicable owner
  gates; every contingency gate SHALL state its classification and cause.

### Evidence, security, and stops

- **YCH-EVD-001:** This specification candidate SHALL claim at most rung 1
  static/schema evidence.
- **YCH-EVD-002:** Future focused tests MAY reach rung 2 but SHALL NOT establish
  integration, provider, hosted, human/usability, pilot, production, or measured
  efficiency evidence.
- **YCH-EVD-003:** Handoffs, receipts, fixtures, and logs SHALL contain no
  secrets, credentials, sensitive provider payloads, or fabricated evidence.
- **YCH-STP-001:** Fixed-point drift, foreign state, truth conflict, material
  ambiguity, sensitive-data risk, missing canonical owner, allowlist expansion,
  unavailable required route, v3 failure at a required boundary, harness
  defect, unexpected RED, or incomplete evidence SHALL stop fail-closed.
- **YCH-STP-002:** No PASS, task, handoff, v3 verification, receipt, review,
  acceptance, commit, or push SHALL authorize its successor.

## Acceptance Matrix

| Concern | Requirement IDs | Primary proof |
|---|---|---|
| canonical language | `YCH-TERM-*` | exact definitions and contradiction tests |
| gate budgets | `YCH-BUD-*` | canonical SDD matrix and negative fixtures |
| bundles and dispatch | `YCH-AUT-*` | authority wording plus forbidden-duty tests |
| retry and harness | `YCH-RET-*` | retry cardinality and auto-repair negatives |
| CompactHandoff selection | `YCH-HND-*` | selection matrix, version check, trust negatives |
| delivery | `YCH-DLV-*` | exact inventory and validator RED/GREEN evidence |
| review and close | `YCH-VAL-*`, `YCH-REV-*`, `YCH-CLS-*` | focused tests, fresh `FULL`, owner decision |
| evidence and stops | `YCH-EVD-*`, `YCH-STP-*` | Receipt Capsule and classified stop fixtures |
