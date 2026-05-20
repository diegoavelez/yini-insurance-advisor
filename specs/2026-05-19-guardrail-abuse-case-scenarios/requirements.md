# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 9 — Guardrails`.

The goal is to add regression-style abuse-case scenarios for the implemented
query-scope, citation-presence, confidence-consistency, and prompt-injection
guardrails.

This slice should stay focused on scenario coverage and validation only. It
should not add new guardrail heuristics or telemetry aggregation behavior.

## In Scope

- Add abuse-case scenarios for already-implemented guardrails.
- Validate that unsafe or boundary-seeking prompts produce the expected guarded outcomes.
- Validate that benign supported prompts still pass normally.
- Keep the scenarios deterministic and regression-oriented.

## Out of Scope

- New prompt-injection heuristics.
- New scope-classification heuristics.
- Telemetry aggregation or summary views.
- MCP exposure.
- UI redesign beyond asserting current surfaced outcomes.

## Execution Model

This slice should validate the existing guarded surfaces.

At minimum:

1. A curated set of unsafe or boundary-seeking prompts is exercised.
2. Each prompt is asserted against the currently expected guarded outcome.
3. A small benign control set is asserted to continue passing normally.
4. The resulting suite is deterministic and suitable for regression checks.

## Abuse-Case Scenario Contract

Scenario coverage must be explicit and deterministic.

At minimum:

- scenarios should map to implemented guardrails only;
- each scenario should assert the expected outcome class, not only that the request fails;
- the slice should not silently broaden scope into evaluation-dataset work.

## Validation Contract

The scenario suite must remain targeted and actionable.

At minimum:

- scenarios should cover unsupported-query refusal;
- scenarios should cover prompt-injection refusal;
- scenarios should cover citation-presence downgrade behavior;
- scenarios should cover confidence-consistency downgrade behavior;
- benign supported controls should still pass.

## Acceptance Criteria

- Deterministic abuse-case scenarios exist for implemented guardrails.
- Expected guarded outcomes are asserted explicitly.
- Benign supported controls remain green.
- The slice stops before telemetry-summary or Phase 10 evaluation work.
