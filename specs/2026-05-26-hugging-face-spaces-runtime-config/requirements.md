# Requirements

## Status

- Drafted.

## Objective

Add the next `Phase 14` deployment slice by defining the minimal Hugging Face Spaces runtime configuration for the current public demo.

## Scope

This slice must cover only:

- the minimal Hugging Face Spaces runtime/config surface for the current app;
- explicit runtime expectations for the chosen Spaces target;
- repository-side configuration that identifies how Spaces should run this app.

This slice must not include:

- broader launch artifact wiring beyond the runtime config itself;
- deployment guide prose;
- rollback notes;
- hosted smoke validation.

## Functional Requirements

1. Spaces Runtime Target
   - Define the Hugging Face Spaces runtime target for the current demo.
   - The chosen target must align with the current Python/Gradio app path.

2. Minimal Config Surface
   - Add the minimal repository-side config file or metadata required to express the Spaces runtime choice.
   - The config must make the intended runtime explicit rather than implicit.

3. Runtime Expectations
   - Document the expected runtime assumptions within the slice artifacts, including the app type and any essential environment/runtime expectation needed by Spaces.

4. Narrowness
   - The slice must stop at runtime configuration.
   - Launch artifacts and deployment instructions belong to later slices.

## Acceptance Criteria

- A minimal Hugging Face Spaces runtime configuration exists in the repo.
- The config is aligned with the current Gradio/Python app path.
- The slice remains scoped to runtime config only.
