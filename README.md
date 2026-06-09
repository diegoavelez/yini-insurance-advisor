---
title: Yini Insurance Advisor
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# Yini

Yini is an internal assistant designed to help senior insurance advisors
retrieve, analyze, compare, and summarize information from official Sura
insurance policy and procedure documents.

This repository now contains the completed `Phase 0` foundation, the full
`Phase 1` configuration and shared-contract slices, the implemented `Phase 2`
and `Phase 3` ingestion/chunking pipeline, the full `Phase 4` embedding and
indexing pipeline, the completed `Phase 5` MVP QA layer, the completed
`Phase 6` observability foundation, the completed `Phase 7` reusable tooling
layer, the completed `Phase 8` workflow orchestration layer, the completed
`Phase 9` guardrail layer, the implemented `Phase 10` evaluation foundation,
the completed `Phase 11` optimization foundation, the completed `Phase 12`
MCP foundation, the completed `Phase 13` demo hardening work, and the
completed `Phase 14` deployment hardening work, the completed `Phase 15`
final evaluation and cleanup work, the completed `Phase 16` ingestion runtime
remediation work, and the completed `Phase 17` runtime compatibility
hardening work.

## Source Documents

- `PRD.md` is the product requirements source of truth.
- `specs/mission.md` contains product principles and anti-goals.
- `specs/tech-stack.md` contains stack constraints and architecture boundaries.
- `specs/roadmap.md` contains implementation order and current build status.
- `specs/` also contains dated implementation specs.

## Current Status

- `Phase 0` through `Phase 17` are complete.
- Detailed implementation status lives in `specs/roadmap.md`.

## Local Setup

Use a local virtual environment for all development.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e '.[dev]'
cp .env.example .env
```

If `python3.11` is not on your shell path, use any Python 3.11+ executable
instead. The project does not support Python 3.10.

## Common Commands

```bash
make setup
make lint
make test
make app
```

## Hugging Face Spaces Deployment

This repo is currently configured for a Docker-based Hugging Face Space.

Authoritative deployment surfaces:

- root `README.md` YAML block:
  - `sdk: docker`
  - `app_port: 7860`
- root `Dockerfile`

Minimal operator procedure:

1. Create a new Hugging Face Space and choose the `Docker` SDK.
2. Push this repository to the Space repository, preserving the root
   `README.md` YAML block and root `Dockerfile`.
3. In the Space settings, configure the runtime secrets or variables required
   by the current startup contract:
   - `GROQ_API_KEY`
   - `GROQ_MODEL`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
4. Let the Space rebuild automatically after the push completes.
5. Confirm the Space serves the app on port `7860`, matching `app_port` in the
   root `README.md`.

Notes:

- The Space runtime uses the root `Dockerfile` as the authoritative build
  artifact.
- Each new commit pushed to the Space repository triggers a rebuild and restart.
- This section is intentionally limited to deployment procedure only; demo
  operating constraints and rollback notes are documented in later slices.

## Deployment Rollback Notes

These notes cover only the minimum rollback guidance for the current hosted
demo deployment path.

Current rollback posture:

- the hosted target remains a Hugging Face Space configured with:
  - `sdk: docker`
  - root `Dockerfile`
- the practical rollback unit is a previously known-good repo state
- restoring that known-good repo state to the Space repository triggers a new
  rebuild of the hosted demo

Minimum rollback procedure:

1. Identify the last known-good commit for the Space repository.
2. Restore or re-push that repo state to the Space repository.
3. Preserve the authoritative deployment surfaces in the restored state:
   - root `README.md` YAML block
   - root `Dockerfile`
4. Confirm the required runtime variables are still configured in the Space:
   - `GROQ_API_KEY`
   - `GROQ_MODEL`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
5. Let the Space rebuild from the restored repo state.

Boundary for this section:

- this section is intentionally limited to rollback guidance
- hosted smoke expectations, runtime/dependency notes, and demo constraint
  notes are documented in separate slices

## Demo Runtime and Dependency Constraints

These notes cover only the hosted demo runtime/dependency posture for the
current Docker-based Hugging Face Space.

Current runtime assumptions:

- hosted target remains a Hugging Face Space configured with:
  - `sdk: docker`
  - `app_port: 7860`
- the authoritative build artifact is the root `Dockerfile`
- the authoritative app entrypoint is:
  - `python -m app.ui`

Current startup-variable contract:

- `GROQ_API_KEY` must be present at runtime
- `GROQ_MODEL` must be present at runtime or resolve to the validated default
  `openai/gpt-oss-120b`
- `QDRANT_URL` must be present at runtime
- `QDRANT_API_KEY` must be present at runtime

Current dependency/runtime constraints:

- the container runtime must expose port `7860`, matching the root `README.md`
  Spaces config and the root `Dockerfile`
- the current image is dependency-heavy and includes ML/document-processing
  packages pulled during `pip install .`; build times and image size should be
  expected to be non-trivial
- local container validation used dummy provider values only for startup and
  readiness checks; a hosted demo still requires real provider configuration
  to support live retrieval and answer generation

Boundary for this section:

- this section is intentionally limited to runtime and dependency constraints
- demo guardrail/supported-scope notes and rollback notes are documented in
  later slices

## Demo Guardrail and Refusal Constraints

These notes cover only the hosted demo guardrail/refusal posture for the
current public advisor surface.

Current guardrail/refusal behavior:

- prompt-injection-style queries are refused conservatively before the normal
  grounded-answer path runs
- answer-generation paths that lose citation traceability are downgraded to a
  lower-confidence draft instead of being presented as normal grounded output
- overstated confidence is downgraded before the final draft is surfaced in
  the demo UI

Current user-visible effect:

- conservative guardrail paths remain draft-oriented and review-oriented rather
  than presenting themselves as fully grounded final answers
- the demo surfaces these outcomes through:
  - limitations
  - trace summary
  - support context
  - debug metadata
  - answer-quality messaging

Boundary for this section:

- this section is intentionally limited to guardrail/refusal constraints
- supported-scope notes, runtime/dependency constraints, and rollback notes
  are documented in separate slices

## Demo Supported-Scope Constraints

These notes cover only the hosted demo supported-scope boundary for the
current public advisor surface.

Current supported-scope posture:

- the demo is intended for grounded questions about supported insurance-policy
  and procedure documents in the current advisor surface
- requests outside that supported insurance-document scope are refused before
  the normal grounded-answer path runs
- unsupported requests are surfaced as low-confidence draft-oriented responses,
  not as normal grounded answers

Current user-visible effect:

- unsupported-scope outcomes appear through:
  - limitations
  - trace summary
  - support context
  - debug metadata
  - answer-quality messaging
- unsupported requests do not proceed into the normal grounded-answer
  generation path

Boundary for this section:

- this section is intentionally limited to supported-scope constraints
- runtime/dependency notes, guardrail/refusal notes, and rollback notes are
  documented in separate slices

## Hosted Smoke Expectations and Operator Notes

These notes cover only the minimum hosted smoke expectations for the deployed
demo and the narrow operator checks to run after a deployment or rebuild.

Current hosted smoke expectations:

- the Space should serve the app on port `7860`
- the public UI should render the current demo surfaces, including:
  - `Service Readiness`
  - `Answer Quality`
  - `Error State`
- the hosted readiness surface is expected to report:
  - `Service Readiness — Ready for grounded draft generation.`
- a benign in-scope query is expected to keep:
  - `Answer Quality — Standard draft quality.`
  - `No active errors.`
  - `This response is a draft for advisor review.`

Minimum operator checks after deploy/rebuild:

1. Open the hosted Space and confirm the app loads successfully.
2. Confirm the page renders the current demo UI sections, especially:
   - `Service Readiness`
   - `Answer Quality`
   - `Error State`
3. Confirm the readiness surface reports the ready state rather than a degraded
   runtime message.
4. Submit one benign in-scope insurance-document query and confirm:
   - the response returns as a draft;
   - no active error state is shown;
   - answer quality remains the standard draft state.

Boundary for this section:

- this section is intentionally limited to hosted smoke expectations and
  operator checks
- rollback guidance, runtime/dependency notes, and demo constraint notes are
  documented in separate slices

## Gradio MVP UI

The current app entrypoint is a thin Gradio layer over the grounded QA backend.

Canonical command:

```bash
python -m app.ui
```

The UI exposes:

- advisor question input
- suggested grounded answer
- citations
- confidence
- limitations
- status / advisor-review messaging

User-visible failure behavior:

- blank input returns an explicit prompt to enter a question
- insufficient evidence remains a typed low-confidence response
- retrieval or generation failures surface as explicit UI errors

## Ingestion CLI

The first implemented `Phase 2` slice is an admin-only offline ingestion job.

Canonical command:

```bash
python -m rag.ingestion ingest-pdfs \
  --input-dir data/raw \
  --markdown-dir data/markdown \
  --processed-dir data/processed \
  --manifest-path data/processed/ingestion-manifest.jsonl \
  --glob "*.pdf" \
  --overwrite false \
  --fail-fast false
```

Required flags:

- `--input-dir`
- `--markdown-dir`
- `--processed-dir`
- `--manifest-path`

Optional flags:

- `--glob` defaults to `*.pdf`
- `--overwrite` defaults to `false`
- `--fail-fast` defaults to `false`
- `--metadata-overlay-path` allows optional operator-curated metadata keyed by
  stable `source_pdf_id`

The command exits non-zero when:

- Docling is not importable in the local runtime
- the input directory does not exist
- no matching PDF files are found
- a conversion fails while `--fail-fast=true`

## Corpus Metadata Baseline

The current corpus identity and metadata contract is intentionally narrow and
deterministic.

Current document-level fields:

- `source_pdf_id` is the stable corpus identity key used across processed
  metadata, chunk artifacts, embedding artifacts, indexing manifests, and
  retrieval payloads
- `source_pdf_relative_path` preserves traceability back to the nested raw
  source tree under `data/raw`
- `document_name` is a retrieval-facing display label:
  - it falls back to the source PDF stem;
  - it upgrades to the first Markdown heading when one is extracted safely
    during ingestion;
  - persisted records still fall back to `source_pdf_id` if no display label is
    available
- `document_version` is optional:
  - it remains unset when no safe version-like token is detected;
  - it is populated only from conservative pattern matching over early document
    text

Current repository responsibilities:

- preserve deterministic artifact naming from `source_pdf_id`
- preserve raw-to-processed traceability through `source_pdf_relative_path`
- carry `document_name` and optional `document_version` through chunk,
  embedding, indexing, retrieval, and citation-facing seams

Current limitations:

- the practical corpus identity surface still depends primarily on
  `source_pdf_id`
- `document_name` quality depends on filename quality or the presence of an
  early heading in extracted Markdown
- `document_version` is best-effort only and may remain absent for many real
  documents
- richer metadata normalization and automatic classification are not yet
  implemented
- operator-curated metadata overlays now exist as an optional ingestion-time
  seam, but they still depend on deliberate manual maintenance

## Repository Layout

```text
app/        Gradio MVP application entry point
agents/     Future LangGraph agents
contracts/  Shared typed contracts across ingestion, retrieval, and answers
core/       Settings and logging bootstrap
data/       Raw, markdown, processed, and eval data
docs/       Supporting durable documentation
mcp/        Future MCP server/client modules
ops/        Guardrails and observability modules
rag/        Ingestion and future retrieval pipeline
specs/      Constitution and implementation specs
tests/      Smoke tests and future test coverage
```

## Next Milestones

`Phase 15` is complete in
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/specs/roadmap.md`.

The next implementation work should start from a new dated spec bundle if
additional scope is approved, with likely follow-on work around:

- expanded product scope beyond the current demo boundary
- new architecture or deployment decisions
- post-demo operational hardening
