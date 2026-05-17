# AGENTS.md

These rules apply to every task unless explicitly overridden.

---

# 1. Core Principles

## Think Before Coding
- Do not start coding immediately for non-trivial tasks.
- State assumptions explicitly.
- If requirements are ambiguous, ask or propose the safest reversible assumption.
- Prefer clarity over speed.

## Simplicity First
- Implement the minimum viable solution that fully solves the problem.
- Avoid speculative abstractions.
- Do not introduce frameworks, patterns, or layers without clear justification.
- Prefer explicit code over clever code.

## Surgical Changes
- Touch only the files required for the task.
- Avoid unrelated refactors.
- Preserve existing architecture and conventions unless explicitly instructed otherwise.
- Keep diffs small and reviewable.

## Read Before Write
Before modifying code:
- Read related modules.
- Read exports and immediate callers.
- Understand existing utilities and patterns.
- Do not duplicate existing functionality.

## Conformance Over Preference
- Match the repository's conventions and patterns.
- Do not silently introduce personal preferences.
- If a convention appears harmful, surface it explicitly instead of bypassing it.

## Fail Loud
- Never hide uncertainty.
- Never claim completion if anything was skipped.
- Explicitly report:
  - skipped tests
  - assumptions
  - unresolved risks
  - partial implementations

## Environment Rules
- Always assume local development uses `.venv`
- Never install dependencies globally
- Use requirements.txt or pyproject.toml as source of truth
- Docker is used for deployment and reproducibility, not as the primary local iteration environment

---

# 2. Spec-Driven Development Rules

## Specs Are Source of Truth
- For non-trivial work, implementation must follow an explicit spec.
- Do not implement undocumented behavior.
- If no spec exists for complex work, request or create one before implementation.

## Map Code to Acceptance Criteria
- Every implementation should trace back to explicit acceptance criteria.
- If acceptance criteria are unclear, stop and clarify.

## Stop on Spec Conflicts
- If the spec conflicts with the codebase, architecture, or existing behavior:
  - stop
  - explain the conflict
  - propose options
- Do not silently resolve contradictions.

## Prefer Incremental Delivery
- Implement work in small verifiable phases.
- Avoid large all-at-once implementations.

---

# 3. Planning Workflow

## Plan First
Enter planning mode when:
- the task involves 3+ steps
- multiple files
- architecture decisions
- production-impacting behavior
- unclear requirements

Plans should include:
- objective
- affected files
- risks
- assumptions
- verification strategy

## Re-Plan When Needed
- If implementation diverges significantly from the plan:
  - stop
  - summarize current state
  - propose a revised plan

## Keep Context Clean
For complex work, separate:
- exploration
- implementation
- debugging
- review
- documentation

Use separate sessions when useful.

---

# 4. Verification Rules

## Never Mark Work Complete Without Verification
Before completion:
- run relevant tests
- run linters/type checks if available
- verify behavior manually when appropriate
- inspect logs/errors when debugging

## Tests Must Verify Intent
- Tests should validate business intent, not only implementation details.
- Prefer behavior-focused tests over brittle implementation-coupled tests.

## Report Verification Explicitly
Always summarize:
- tests run
- commands executed
- files changed
- verified outcomes
- remaining risks

---

# 5. Bug Fixing Rules

## Fix Root Causes
- Avoid cosmetic or temporary fixes.
- Investigate the underlying issue before patching symptoms.

## Use Evidence
- Use logs
- failing tests
- stack traces
- runtime behavior
- CI output

Do not guess blindly.

## Minimize Impact
- Prefer the smallest safe fix that resolves the root cause.

---

# 6. Documentation Rules

## Keep Durable Knowledge in Files
Persistent project knowledge belongs in:
- docs/
- specs/
- architecture notes
- decisions/
- tasks/lessons.md

Do not rely only on conversational context.

## Lessons Learned
Update lessons documentation only when:
- a mistake repeats
- a workflow fails
- an architectural lesson emerges
- a project-specific pattern becomes important

Avoid noisy documentation.

---

# 7. Token and Context Discipline

## Preserve Context Quality
- Keep responses concise and operational.
- Avoid unnecessary explanations during execution.
- Summarize progress periodically for long tasks.

## Prefer Fresh Context Over Long Drift
If context becomes noisy or inconsistent:
- summarize current state
- start a fresh execution context

---

# 8. Definition of Done

A task is complete only if:
- implementation matches the spec
- acceptance criteria are satisfied
- relevant tests pass
- changes are documented when needed
- assumptions and risks are reported
- no important step was skipped silently