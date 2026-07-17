# Executor Workflow

## Purpose

Executor tasks perform bounded work on behalf of the Yini master thread. They do
not choose the next strategic unit and do not inherit publication or external
authority from implementation instructions.

## Handoff Contract

Every executor handoff must state:

- objective and explicit non-goals;
- exact repository and starting branch or commit;
- active requirements and validation sources;
- allowed files or bounded surface;
- assumptions and known unknowns;
- acceptance criteria and verification commands;
- permitted authorities: planning, edits, verification, commit, push,
  provider-backed execution, deployment, and external actions;
- fail-closed conditions and required return evidence.

If the requested work cannot stay inside this contract, stop and return the
scope conflict instead of widening the task.

## Execution Rules

An executor must:

1. run a live Git preflight before editing;
2. read the active spec, related modules, callers, exports, and tests;
3. preserve existing and foreign changes;
4. implement only documented behavior;
5. keep changes minimal and reversible;
6. run acceptance checks proportionate to risk;
7. avoid credentials, providers, deployment, and network activity unless
   explicitly authorized;
8. stop on drift, sensitive-data risk, conflicts, or material ambiguity;
9. avoid opening the next slice or making portfolio decisions.

## Return Contract

The executor must return:

- outcome and acceptance status;
- exact files changed;
- concise diff summary;
- commands executed with pass/fail results;
- skipped or unavailable checks;
- current branch, `HEAD`, upstream divergence, and worktree state;
- commit hash if a commit was explicitly authorized and created;
- publication targets if a push was explicitly authorized and completed;
- remaining risks, blockers, and the evidence ceiling;
- the decision now required from the master thread.

Claims must not exceed the evidence. Local tests cannot be reported as hosted or
provider-backed validation.

## Review and Acceptance

The master thread compares the return package with the originating requirements
and validation contract. A clean diff or passing test suite is necessary but
does not by itself authorize acceptance, commit, publication, deployment, or the
next slice.
