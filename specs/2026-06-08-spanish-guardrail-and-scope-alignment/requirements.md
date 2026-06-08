# Requirements

## Feature Summary

This feature defines the third narrow implementation slice of
`Phase 15 — Final Evaluation and Cleanup`.

The goal is to align deterministic query-scope classification and
prompt-injection guardrail detection with Spanish-speaking demo usage, without
changing broader evaluation assets, answer-generation prompts, or non-Spanish
product behavior beyond the necessary deterministic matching expansion.

This slice must stay focused on deterministic scope and guardrail alignment.

## In Scope

- Expand supported query-scope token matching to cover common Spanish
  insurance-document queries.
- Expand deterministic prompt-injection signal patterns to cover common Spanish
  override/reveal formulations.
- Add or update targeted tests that verify Spanish supported-scope and
  prompt-injection behavior.
- Preserve current refusal/result contracts and current event names.

## Out of Scope

- Embedding-model changes.
- Evaluation dataset rewrites.
- Prompt/completion generation redesign.
- Broader multilingual generalization beyond the deterministic Spanish patterns
  needed for the demo.
- Hosted deployment changes.

## Alignment Expectations

At minimum:

- common Spanish insurance terms should not be misclassified as unsupported
  solely because they are not English;
- common Spanish prompt-injection formulations should trigger the same narrow
  conservative refusal path as the current English patterns;
- the slice should preserve the current typed decisions and guardrail event
  surfaces.

## Acceptance Criteria

- Spanish insurance-document questions can satisfy deterministic supported-scope
  matching.
- Spanish prompt-injection formulations trigger deterministic guardrail refusal.
- Existing English deterministic behavior remains intact.
- The slice stops before evaluation-dataset and broader prompt changes.
