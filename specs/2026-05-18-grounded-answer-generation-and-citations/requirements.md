# Requirements

## Feature Summary

This feature defines the second narrow implementation slice of
`Phase 5 — Basic RAG MVP`.

The goal is to generate the first grounded draft answers from retrieved
evidence and return explicit citations without yet expanding into UI-heavy or
multi-agent orchestration work.

This slice should turn the existing typed retrieval pipeline into the first
end-to-end grounded QA path.

## In Scope

- Construct answer-generation prompts from retrieved evidence.
- Use the configured Groq model for grounded answer generation.
- Map model output into the existing typed response contracts.
- Return explicit citations derived from retrieved evidence.
- Define failure behavior for empty, weak, or insufficient retrieval context.
- Add the first narrow end-to-end grounded QA workflow seam.

## Out of Scope

- Multi-agent orchestration.
- Query rewriting.
- Complex tool routing.
- Rich Gradio interaction patterns.
- Advanced guardrails beyond basic grounded-response boundaries.
- Retrieval re-ranking changes.

## Execution Model

This slice may remain callable from CLI or internal pipeline seams, but it must
stay:

- typed;
- independently testable;
- explicitly configured;
- reusable by later app and orchestration layers.

The execution path for this slice should be:

1. Accept a user query.
2. Retrieve ranked evidence through the existing retrieval pipeline.
3. Build a grounded prompt from the retrieved evidence.
4. Generate a draft answer through Groq.
5. Return a typed grounded response with citations and limitations.

## Configuration Contract

This slice must use the typed settings contract in `core.config.Settings`.

At minimum:

- `GROQ_API_KEY` must be required when answer generation is requested;
- `GROQ_MODEL` must be required and explicit;
- retrieval prerequisites must still be validated because answer generation
  depends on retrieval;
- config failures must fail loudly before model invocation.

## Input Contract

This slice should accept a typed user-query input and rely on the existing
typed retrieval query/result contracts.

At minimum, the grounded-answer path must preserve:

- original user query;
- ranked retrieved chunks;
- retrieval ordering;
- traceable chunk metadata for later citation output.

The public interface must remain typed and must not require raw prompt strings
from callers.

## Output Contract

This slice should use the existing response and verification contracts where
possible.

At minimum, the grounded-answer output should include:

- suggested answer text;
- citations;
- confidence level;
- explicit limitations when evidence is partial;
- advisor review notice.

The response must remain grounded in retrieved evidence rather than free-form
model output.

## Citation Contract

This slice should make citations explicit in the returned answer structure.

At minimum:

- citations should be derived from retrieved evidence, not fabricated;
- citation metadata should preserve document name and any available section,
  page, or clause identifiers;
- if evidence is insufficient for a strong answer, the response should reflect
  that limitation explicitly rather than fabricate support.

## Prompt Construction Contract

This slice should define a deterministic prompt-building seam.

At minimum:

- retrieved chunks should be included in a stable order;
- prompt construction should preserve traceability to chunk identifiers or
  source metadata;
- the prompt should instruct the model to stay within provided evidence;
- prompt assembly should be testable without live model calls.

## Failure Behavior

If answer generation fails:

- failures must be explicit and not treated as successful grounded answers;
- missing retrieval evidence must be distinguishable from model/runtime errors;
- insufficient evidence should produce a typed limited response or an explicit
  failure policy, not silent hallucination.

## Smoke Validation

This slice should include narrow grounded-QA smoke validation.

At minimum:

- a successful path proves retrieval plus answer generation can execute;
- returned answers are typed and include citations;
- empty or weak retrieval inputs do not yield silently overconfident answers.

## Acceptance Criteria

- The system can generate a first grounded draft answer from retrieved chunks.
- Citations are explicit and traceable.
- Groq config is validated through `Settings`.
- Prompt construction is deterministic and testable.
- Failure and insufficient-evidence behavior are explicit.
- The slice stops before UI expansion and orchestration work.
