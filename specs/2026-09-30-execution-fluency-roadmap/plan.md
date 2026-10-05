# Execution Fluency Roadmap — Plan

## Current documentary pass

Objective: specify all four finite fronts with testable contracts and minimal
owner decisions. Affected paths: only the five files in this directory.
Assumptions: principal checkout, fifteen explicitly permitted foreign deltas,
empty staging, trusted Python/Git/v1 observer, no relevant ignored inputs.
Risks: overstating historical evidence, changing policy by implication,
conflating transcribed bytes with a changed oracle, circular bootstrap and
accidental cross-repo action. Verification: static traceability, local links,
UTF-8/LF/whitespace, exact scope and protected-byte/Git/config preservation.

One v1 invocation precedes writes; no repeat. Use apply_patch for documents.
Current finite counters: up to 2 eligible identical transient pre-mutation
retries, 1 invocation-only harness repair without changed oracle, 2 in-scope
documentary correction cycles after validation. These do not relax observer
STOP. No product tests, temporary artifacts, installs or successor tasks.

## Dependency graph and owner gates

```text
S0 this specification -> owner spec disposition
  |-> F1-I bootstrap TDD -> F1-R independent review -> owner F1 acceptance
  |       -> F1-L separately granted read-only integration -> F1-LR review
  |       -> owner integration disposition -> F2-O canonical adoption
  |-> F2-D guidance scenarios ---------------------> F2-O
  |-> F3-O current-state/byte reconciliation (can run first, uses existing v1)
  |-> F4-D local plugin proposal
F2-O, F3-O, F4-D -> proportional fresh independent reviews -> owner acceptance
accepted F1 mechanism + integration + F2 adoption + F3 reconciliation
  + F4 local readiness -> local roadmap closed
F4 readiness -- optional exact transfer grant --> external AgentOps master
external adoption -- separate later Yini decision --> optional local adoption
v3/publication: separate existing roadmap, no dependency to local closure
```

These are logical nodes, not automatically created chats or approval demands.
F2-D may be authored with F1-I under one explicitly scoped objective; F2-O,
F3-O and F4-D may share a documentary objective after their prerequisites,
with exact union allowlist and individual closure evidence. Reviews stay
independent. F3 may instead close first without waiting for F1-L. Never make
an already completed F3 wait for unrelated integration or external response.

Normal owner gates follow the existing Level 2 cadence: this spec-creation
decision, then spec acceptance plus separately named delivery grants,
independent review authority, final acceptance plus any separately named
adoption/close grants. With accepted applicable spec, the local core has
three normal owner gates. A grouped decision can name multiple exact tasks
and ordered successor preconditions; it cannot delegate future unknown scope
or renew a terminal grant. Integration, adoption and their reviews can be
named in such groups only when exact preconditions are bound. Contingency
decisions are reported separately; task count is not approval-gate count.

## Future footprint and validation

Every row is PROPOSED, not an edit grant. Fresh dispatch binds exact paths,
accepted spec bytes, complete predecessor identity and trusted runtimes.

| Node | Candidate paths | Required evidence |
|---|---|---|
| F1-I | scripts/execution_contract.py; tests/test_execution_contract.py; this validation.md evidence append | Public-seam TDD T01–T10; v1/v2 regression command |
| F1-L | No code/config writes; this validation.md append only if separately named | Single controlled eligible v1 invocation via accepted transport; complete native result; preserved state |
| F2-D/F2-O | docs/agents/executor-workflow.md; this validation.md; specs/roadmap.md pointer at adoption | T11–T12 guidance scenarios, static consistency, existing governance validator |
| F3-O recommended | docs/operations/execution-state.md; specs/roadmap.md; prior staged-preflight spec.md and validation.md dated addenda; this validation.md | T13–T14, unchanged receipts and chosen tasks.md bytes |
| F3-O exact restoration | Recommended paths plus prior staged-preflight tasks.md | T13–T14 plus exact literal bytes/digest before and after |
| F4-D | docs/operations/proposals/agentops-literal-transcription-clarification.md; this validation.md | T15–T16 local content and transfer-boundary scenarios |

No planned changes to AGENTS, master-control, ADR 0001, metrics, receipt
policy/index, v1/v2 implementation/tests, plugin or configuration. If any
becomes necessary, return a scope decision. In particular, a pre-existing
governance-validator failure is classified with evidence; do not silently
edit its markers/tests or widen the candidate to obtain green.

Exact future commands, run from verified principal checkout, not run by S0:

```sh
/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.venv/bin/python -B -m unittest discover -s tests -p 'test_execution_contract.py'
/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.venv/bin/python -B -m unittest discover -s tests -p 'test*readonly_preflight.py'
/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.venv/bin/python -B scripts/validate_master_control.py --repo /Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor
```

Inspect fixture isolation and verify .venv's physical runtime/hash before a
future dispatch. Missing runtime is a stop, not installation authority.
No make test-release or product suite is needed for this surface. Run focused
checks after edits and at most one final proportional selected suite per
objective; an unchanged PASS needs no ceremonial rerun. The governance
validator is static evidence, not proof of runtime permissions or every prose
invariant. Supplement it with the explicit T11–T16 documentary scenarios.

F1-L uses the accepted physical Python with `-B`, absolute new script,
`prepare` then `invoke`, exact request bytes through stdin and no shell
substitution. Its fresh grant must bind complete current source contract,
source/derived digests, Python/script/Git identities, coverage, empty staging,
configuration preservation and one invocation. A command template alone is
not an executable grant. Missing coverage stops before invocation.

## Bootstrap without circular trust

F1-I is authorized against the existing accepted v1 observer and the explicit
three-call bootstrap in its plan. Verify v1 once with the fresh owner-bound
contract before editing the new transport. Build public pure seams using
invented byte fixtures and subprocess/OS boundary doubles. Then exercise
main/invoke with independently specified outputs and launch counts. No real
Git initialization, mutation or private observer-helper mocks in those tests.

The new mechanism cannot preflight its own initial implementation or accept
itself. F1-R reviews exact code, test oracles and actual RED/GREEN evidence.
Only after owner acceptance can F1-L call it against the real principal
checkout under read-only authority. F1-L reaches bounded integration only;
F2-O's later accepted canonical pointer makes the eligible v1 transport the
normal reusable path. Until then existing exact dispatch remains available.

## Completion and decisions

F1 closes with accepted tested mechanism, controlled read-only integration
and accepted adoption pointer. F2 closes with accepted guidance and scenario
evidence demonstrating finite continuation without added mechanical approval.
F3 closes with accepted current projection and explicit byte disposition.
F4 closes locally with accepted transfer-ready proposal; external transfer
and adoption remain optional separate actions. Global close records those
four predicates, their evidence ceilings, residual risks and next owner choice.
No promise of absolute fluency or measured savings is part of completion.

Recommend accepting the specs, selecting F3's unchanged-LF disposition, and
authorizing an exact F3 documentary objective first if immediate reconciliation
is desired, alongside separately named F1 bootstrap work when ready. Owner
may group decisions without making one task grant another. This proposal
does not dispatch those tasks or modify the global roadmap today.

## Prospective routing-validator dependency — 2026-09-30

Owner-authorized expansion: `YINI-FLUENCY-ROUTING-VALIDATOR-ALIGNMENT-1`,
dispatch owner `019f71d6-632c-7870-bfa2-89513fdeb85a`, principal checkout,
route `gpt-6.1-sol / medium`. This addendum supersedes only the earlier
exclusion of governance-validator edits for this separately named dependency;
the original planning and validation history remains unchanged.

The executor-workflow already owns the approved Sol 6.1 Medium/High routes.
Align the two stale required markers in `scripts/validate_master_control.py`
and the invented fixture/regressions in `tests/test_validate_master_control.py`.
The exact allowlist is those two paths plus this plan and validation.md for
append-only dependency/evidence records. Do not edit routing policy or add
obsolete default routes to make the validator pass. Preserve Astra/Luna,
explicit alternatives and silent-substitution controls.

Separate IMPLEMENT and VALIDATE grants form one finite local objective.
Use public validate/CLI TDD, affected routing checks and one final full test
file, then the physical validator and authorized read-only postflight.
Counters: 2 eligible identical transient retries before mutation, 1
invocation-only harness repair without oracle change, 2 semantic corrections
after first complete validation. No observer replay, installation, Git writes,
provider/network action, independent review or acceptance is included.

This dependency removes the known stale-marker obstacle for renewed F1–F4
objectives. It does not renew their stopped grants, implement those fronts or
change their closure predicates. Master/owner alone handles their separately
authorized renewal and coordination. Completion here is
READY_FOR_INDEPENDENT_REVIEW after focused tests, physical validator and
four-path/protected-state preservation pass; evidence reaches rung 2 only.
