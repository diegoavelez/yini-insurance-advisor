# Execution Fluency Roadmap — Specification

Date: 2026-09-30. Work unit: `YINI-EXECUTION-FLUENCY-ROADMAP-SPEC-1`.
Status: `PROPOSED / READY_FOR_OWNER_SPEC_DECISION`, not accepted policy.
SDD Level 2: five documents are sufficient for a small public execution
contract and transversal governance decisions. This is governance work,
not a product slice, service blueprint or production-readiness claim.

Role: specification executor. Dispatch owner:
`019f71d6-632c-7870-bfa2-89513fdeb85a`. Route: `gpt-6-astra / high`.
Required physical repository:
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor`.
Required absolute common-dir:
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.git`.
Principal checkout required; no reselection or redelegation.

## Problem and evidence

The completed audit `YINI-EXECUTION-FRICTION-AUDIT-1`, thread
`01a0f475-4599-7aa0-ad68-83b0286d722f`, is the decision source. Its final
agent message and native probe `exec-cd194ef3-112f-47ab-ae13-76b32343127c`
(exit 0) distinguish five mechanisms:

1. Contract extraction assumed `role=user` and confused literal `\\n` with LF.
2. A semantically correct string replacement also changed SPACE to LF.
3. The caller passed the observer's internal Git environment to Python.
4. An assertion ran before diagnostic capture, hiding native STOP detail.
5. A principal-file absence assertion was applied to an existing linked file.

The four RED/GREEN probes and linked-absence check used invented in-memory
fixtures, no subprocesses or integration. They establish mechanisms, not a
new candidate PASS. The exact reason for the historical observer exit 4 was
not printed; the forbidden environment is supported evidence, not a recovered
native reason. Two literal-correction tasks accumulated 30 shell executions
and 7 min 03 s of task duration. These are audit context, not token, monetary,
user-time or future-savings measurements. No benchmark program follows.

Master handoffs share responsibility: they prescribed fragile transport and
large bespoke checks, propagated stale semantic state and left literal repair
classification unclear. Executor mistakes and handoff defects must both be
addressed. More models, Full Access and automatic policy relaxation do not
follow from these observations.

## Four finite outcomes

| Front | Initial state | Finite outcome | Canonical owner |
|---|---|---|---|
| F1 reusable mechanics | Existing v1/v2 observers; callers reconstruct transport, environment and capture per chat | Small tested transport module and one stable CLI for eligible v1 invocation, plus pure literal/evidence helpers; adopted only after review and acceptance | New local script/tests; procedural selection in executor-workflow |
| F2 bounded local objective | Opt-in bundle already exists; mechanical confirmations and counters are inconsistently applied | One visible executor per objective with explicit edit/validation grants, finite corrections, proportional independent review and grouped owner decisions | executor-workflow; installed authority-grants owns universal rules |
| F3 O1 reconciliation | Owner acceptance after FULL PASS is transmitted; current state/roadmap still say pending; literal fix has extra LF | Current projection agrees with received acceptance, history remains frozen, exact byte disposition of pending correction is reviewed and accepted | execution-state; roadmap pointer; dated prospective spec addendum |
| F4 plugin proposal | Literal/assertion transcription restoration is not expressly eligible under current invocation-only repair | Locally reviewed proposal with positive/negative examples and transfer conditions, ready for a later authorized AgentOps master handoff | Local proposal; external authority-grants maintainer owns any adoption |

## Decisions fixed by this proposal

Use a standard-library mechanism, not a workflow engine, scheduler, new skill,
CI project or generic command runner. Preserve v1/v2 code, tests and meaning.
Do not implement v3 here or make F3 wait for v3/publication. Build and test the
new mechanism without depending on its own acceptance. Later controlled
read-only integration is a separate named authority.

F2 selects no bundle by default. It documents the already available opt-in
route and adds only proposed local operational guidance. Existing grants keep
their literal terms. No observer STOP is repairable by this roadmap. A changed
oracle never becomes a transcription repair merely because the new value
matches the observed result. F4 seeks a narrow future clarification; pending
external adoption, Yini uses the stricter current rule or a separately named
owner-authorized correction.

No new technical interview is needed. The remaining owner choices are
acceptance, selection of future exact grants and F3's byte disposition, stated
in [requirements.md](requirements.md). They are not hidden implementer choices.

## Scope, assumptions and exclusions

This task creates only this directory's `spec.md`, `requirements.md`,
`plan.md`, `tasks.md` and `validation.md`. Its separate documentary-writing
and consistency/preservation-check grants do not implement the roadmap or
adopt policy. The fifteen inventoried predecessor deltas stay unchanged.
No edits to current canonical documents, observers, tests, configuration,
plugin repo/cache, receipt index or product code are authorized here.

Fixtures use invented/public/explicitly authorized data only. No credentials,
insurance corpus, Qdrant, Hugging Face, provider, network, installation,
deployment, pilot, Git write, external message or tracker action. Hashing
does not authorize reading sensitive data. Unknown data classification stops.

Exclusive checkout use, trusted runtime identities and complete declared
state are assumptions. Filesystem checks are nonatomic; ABA, malicious
concurrent writers and tool bypass remain outside assurance. A deterministic
mechanism validates data, not human authority or runtime permissions.

## Sources and completion

[Requirements](requirements.md) own interfaces and ACs;
[plan](plan.md) owns dependencies, prospective files and validators;
[tasks](tasks.md) owns executor boundaries;
[validation](validation.md) separates observed documentary evidence from
future NOT_RUN scenarios. Governing sources are
[AGENTS](../../AGENTS.md), [adapter](../../docs/agents/agentops-workflow.md),
[executor](../../docs/agents/executor-workflow.md),
[master](../../docs/operations/master-control.md),
[state](../../docs/operations/execution-state.md),
[ADR 0001](../../docs/adr/0001-read-only-master-control-topology.md),
[roadmap](../roadmap.md) and the installed `OPERATING-MODEL.md`,
`authority-grants.md` and `receipt-policy.md` references.

Yini's strictly read-only master overrides the installed model's narrower
state-maintenance exception. Only an authorized executor changes local state.
Current spec completion means five coherent files and verified preservation,
at rung 1. Global roadmap completion requires F1–F4's distinct closure
predicates, including local F4 readiness, not external plugin adoption.
Acceptance of these specs creates no implementation, Git or successor grant.
