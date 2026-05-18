# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- Retrieved evidence can be turned into a deterministic grounded prompt.
- Groq configuration failures fail loudly before model invocation.
- A successful path returns a typed grounded response with citations.
- Citation fields are derived from retrieved evidence and remain traceable.
- Empty or insufficient retrieval results do not produce silently confident
  answers.
- Model/runtime failures are explicit and not treated as grounded success.
- The implementation remains scoped to grounded answer generation, not UI or
  orchestration.

## Merge Readiness

This spec is ready when the second `Phase 5` slice is decision-complete for:

- deterministic prompt construction;
- Groq-backed grounded answer generation;
- typed citation-bearing response outputs;
- explicit insufficient-evidence behavior;
- explicit generation failure handling;

without drifting into UI expansion or agent orchestration.
