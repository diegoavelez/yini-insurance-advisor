# Plan

1. Grounded QA Interface
   - Define the first typed grounded-answer callable seam.
   - Reuse existing retrieval and response contracts where possible.

2. Retrieval Integration
   - Invoke the existing retrieval pipeline as the evidence source.
   - Preserve ranked evidence ordering and traceability metadata.

3. Prompt Construction
   - Add a deterministic prompt-building function for grounded generation.
   - Keep the prompt assembly testable without live Groq calls.

4. Groq Generation Path
   - Validate Groq configuration through `Settings`.
   - Add the first narrow model invocation path for grounded answers.

5. Citation and Limitation Mapping
   - Map retrieved evidence into explicit citations.
   - Add limitation handling for partial or weak evidence.

6. Failure and Empty-Evidence Handling
   - Distinguish retrieval insufficiency from runtime/model failures.
   - Keep failure behavior explicit and typed.

7. Validation Coverage
   - Add tests for prompt construction, typed outputs, citation mapping,
     insufficient-evidence handling, and generation failures.

8. Deferred Work Boundary
   - Explicitly stop before richer UI, multi-agent orchestration, and advanced
     guardrail layers.
