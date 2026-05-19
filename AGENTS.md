# AGENTS.md

These rules apply to every task unless explicitly overridden.

## Core Behavior

- Think before coding.
- For non-trivial tasks, write a short plan before editing.
- Prefer simple, minimal, reversible changes.
- Touch only files required by the task.
- Read related modules, callers, exports, and existing utilities before changing code.
- Match existing conventions over personal preference.
- Surface uncertainty, skipped checks, conflicts, and risks explicitly.
- Do not claim completion unless the work is verified.

## Spec-Driven Development

- Specs are the source of truth for non-trivial work.
- Do not implement undocumented behavior.
- Map implementation to acceptance criteria.
- If specs conflict with code, stop and explain the conflict.
- Deliver work in small verifiable phases.

## Environment

- Use local `.venv` for development.
- Initialize repo with git
- Never install dependencies globally.
- Use `requirements.txt` or `pyproject.toml` as dependency source of truth.
- Docker is for reproducibility and deployment, not the primary local dev loop.

## Planning Rules

Enter planning mode when the task involves:
- 3+ steps;
- multiple files;
- architectural decisions;
- production-impacting behavior;
- unclear requirements.

A plan must include:
- objective;
- affected files;
- assumptions;
- risks;
- verification strategy.

If execution diverges, stop and re-plan.

## Verification

Before marking work complete:
- run relevant tests;
- run linters/type checks when available;
- verify behavior manually when needed;
- report commands executed;
- report files changed;
- report skipped checks.

Tests should verify intent, not only implementation details.

## Bug Fixing

- Find root causes before patching symptoms.
- Use logs, failing tests, stack traces, and CI output.
- Prefer the smallest safe fix.

## Documentation

- Durable project knowledge belongs in `docs/`, `specs/`, `decisions/`, or `tasks/lessons.md`.
- Update `tasks/lessons.md` only for repeated mistakes or project-specific lessons.
- Keep documentation useful, not noisy.

## Definition of Done

A task is done only when:
- it matches the spec;
- acceptance criteria are satisfied;
- relevant checks pass;
- assumptions and risks are reported;
- no important step was skipped silently.