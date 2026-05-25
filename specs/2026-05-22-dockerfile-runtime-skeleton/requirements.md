# Requirements

## Status

- Drafted.

## Objective

Add the first `Phase 14` deployment slice by defining a production-oriented Docker runtime skeleton for the current app path.

## Scope

This slice must cover only:

- one Dockerfile for the current app/runtime path;
- explicit dependency installation from repo source of truth;
- explicit app entrypoint wiring for the current public demo surface;
- a narrow container runtime contract that can be validated locally later.

This slice must not include:

- local container smoke/startup validation;
- Hugging Face Spaces or other hosted-platform wiring;
- deployment rollback notes;
- broader deployment docs beyond what is necessary to understand the Docker runtime contract.

## Functional Requirements

1. Docker Runtime Skeleton
   - Add one top-level `Dockerfile` for the current app.
   - The image must target the existing Python app/runtime path used by the repo.

2. Dependency Installation
   - Dependency installation must use the repo dependency source of truth.
   - The Dockerfile must not rely on globally preinstalled project dependencies.

3. App Entrypoint
   - The Dockerfile must define a clear default runtime entrypoint or command for the current demo app.
   - The entrypoint must be explicit rather than implied by container defaults.

4. Runtime Environment Contract
   - The Dockerfile must declare only the minimal runtime environment surface needed for the current demo path.
   - Any exposed port used by the current app must be explicit.

5. Narrowness
   - The slice must stop at a plausible runtime skeleton.
   - Startup proof and smoke validation belong to the next slice.

## Acceptance Criteria

- A single Dockerfile exists at the repo root.
- The Dockerfile clearly installs dependencies and wires the app startup command.
- The Dockerfile is aligned with the current Python runtime and app entrypoint conventions already present in the repo.
- The slice does not drift into hosted deployment or smoke-validation implementation.
