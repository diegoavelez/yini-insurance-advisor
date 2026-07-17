# Yini Master Control

## Purpose

This document defines the permanent strategic control layer for the Yini
repository. Master control is not an implementation slice. It coordinates work,
keeps the repository state legible, validates executor evidence, and returns
material decisions to the user.

## Truth Sources

Use the following order when deciding what the repository currently permits:

1. explicit user instruction for the current task;
2. `AGENTS.md`;
3. the accepted requirements and validation contract for the active slice;
4. `PRD.md`, `constitution.md`, and `specs/roadmap.md`;
5. `docs/operations/execution-state.md` and other operational documentation;
6. Graphify and other derived analysis artifacts.

If two applicable truth sources conflict, stop and surface the conflict. Do not
silently choose the wider scope.

## Master Thread Responsibilities

The master thread must:

- verify live Git state before authorizing or reviewing work;
- identify the current stage, active unit, evidence ceiling, and blockers;
- keep confirmed facts separate from assumptions and unknowns;
- prepare bounded executor handoffs with explicit acceptance criteria;
- validate returned evidence against the originating spec;
- prevent unrelated work from being mixed into a slice;
- update `docs/operations/execution-state.md` when accepted repository state
  materially changes;
- return stage, scope, release, and publication decisions to the user.

Routine feature implementation should occur in a bounded executor task unless
the user explicitly asks the master thread to implement it.

## Separate Authorities

The following authorities are independent and must be granted explicitly:

1. planning or specification;
2. implementation or documentation edits;
3. local verification;
4. staging and local commit;
5. push to `origin`;
6. push to the Hugging Face `hf` remote;
7. pull request, merge, or branch publication;
8. provider-backed execution or credential access;
9. deployment, hosted smoke tests, or other external actions;
10. Graphify refresh and Graphify artifact commit.

Authorization for a local commit does not authorize a push. Authorization to
push `origin` does not authorize a push to `hf` or a deployment.

## Required Preflight

Before edits, commit, publication, or external execution, verify as applicable:

- current branch, `HEAD`, upstream, and ahead/behind counts;
- exact worktree path set and ownership of existing changes;
- active spec and its acceptance criteria;
- required runtime and `.venv` availability;
- whether credentials, provider access, deployment, or network activity are in
  scope;
- whether Graphify is present and fresh enough to be useful as secondary
  context.

Stop fail-closed on foreign changes, unexpected branch drift, sensitive data,
missing prerequisites, conflicting specs, or material ambiguity.

## Evidence Standard

Completion evidence must report:

- exact files changed;
- commands executed and their results;
- acceptance criteria satisfied;
- checks skipped and why;
- remaining risks or unavailable external evidence;
- Git state after verification.

Local deterministic checks do not prove hosted behavior, provider readiness,
deployment acceptance, or production suitability.

## Strategic Stops

Stop and request a joint decision when:

- a slice closes and the next unit has not been authorized;
- work would expand product scope or change a durable contract;
- acceptance evidence is incomplete or contradicts the spec;
- a push would publish unrelated local commits;
- provider, deployment, customer, or other external activity becomes necessary;
- the evidence ceiling is lower than the claim being requested.
