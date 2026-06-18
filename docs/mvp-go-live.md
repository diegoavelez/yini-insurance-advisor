# MVP Go-Live Baseline

## Purpose

This document is the explicit operational baseline for releasing and operating
the current MVP.

It consolidates the already implemented surfaces for:

- deterministic pre-release verification;
- hosted post-deploy smoke validation;
- rollback posture;
- corpus-update/operator workflow;
- the supported category set that the MVP is shipping with.

This document does not expand product scope. It defines the minimum operational
path for the MVP as it exists today.

## Shipped MVP Scope

The current MVP ships with the following supported category families:

- `ARL`
- `MOVILIDAD/AUTOS`
- `MOVILIDAD/BICICLETAS Y PATINETAS`
- `MOVILIDAD/MOTOS`
- `MOVILIDAD/TRANSVERSALES/choque simple`
- `MOVILIDAD/PV`
- `MOVILIDAD/UTILITARIO Y PESADOS`
- `MOVILIDAD/FINANCIACION`
- `MOVILIDAD/VIAJES`
- `MOVILIDAD/SUSCRIPCION`
- `MOVILIDAD/MUEVETE LIBRE`
- `MOVILIDAD/SOAT`
- `EPS/PAC`

Current corpus boundary:

- ingestion is intentionally PDF-only;
- `.docx` forms are excluded from the MVP corpus and answer surface;
- new categories are not part of this go-live baseline unless they complete the
  onboarding and validation workflow separately.

## Pre-Release Gate

The authoritative deterministic pre-release gate is:

```bash
make test-release
```

This gate is the minimum required local verification pass before release.

It protects:

- evaluation and smoke surfaces;
- MCP compatibility surfaces;
- app, workflow, supported-scope, guardrail, and observability surfaces;
- retrieval, grounded-answer, canonicalization, embedding, indexing, CLI, and
  ingestion seams.

Useful but non-gating checks:

- `make test` for the broader full suite;
- targeted live Qdrant/Groq validation after material runtime or corpus
  changes;
- category-specific onboarding validation through the operator playbook.

## Deployment Baseline

The hosted target is the Hugging Face Space configured from:

- root `README.md` YAML:
  - `sdk: docker`
  - `app_port: 7860`
- root `Dockerfile`

Runtime variables required by the hosted MVP:

- `GROQ_API_KEY`
- `GROQ_MODEL`
- `QDRANT_URL`
- `QDRANT_API_KEY`

Authoritative hosted app entrypoint:

- `python -m app.ui`

## Post-Deploy Hosted Smoke

After each deploy or rebuild, run the minimum hosted smoke:

1. Open the hosted Space and confirm the app loads.
2. Confirm the UI renders:
   - `Service Readiness`
   - `Answer Quality`
   - `Error State`
3. Confirm readiness reports:
   - `Service Readiness — Ready for grounded draft generation.`
4. Submit one benign in-scope query and confirm:
   - a draft answer is returned;
   - no active error state is shown;
   - answer quality remains the standard draft state.

This is the minimum required hosted smoke for the shipped MVP.

## Rollback Baseline

The rollback unit is a previously known-good repo state.

Minimum rollback procedure:

1. Identify the last known-good commit.
2. Re-push or restore that state to the Hugging Face Space repository.
3. Preserve the authoritative deployment surfaces:
   - root `README.md` YAML block
   - root `Dockerfile`
4. Confirm the required runtime variables remain configured.
5. Allow the Space to rebuild from the restored state.

## Corpus Update Baseline

The MVP supports corpus updates only through the existing onboarding/operator
workflow.

Operator source of truth:

- `docs/category-onboarding-playbook.md`

Minimum posture for corpus updates:

1. Keep raw PDFs under stable taxonomy-preserving paths in `data/raw/`.
2. Keep `.docx` files out of ingestion and answer expectations.
3. Run the external batch workflow for ingestion, embeddings, and indexing.
4. Inspect cleaned markdown and chunks before treating a category as ready.
5. Validate at least one real retrieval and one real grounded answer.
6. Open a dated corrective spec if the category requires recovery work.

Do not treat “ingested” as equivalent to “ready for the hosted MVP”.

## Go-Live Checklist

Use this checklist when shipping the current MVP:

1. `make test-release` passes locally.
2. The intended repo state is pushed to `origin` and `hf`.
3. The Hugging Face Space rebuild completes successfully.
4. Hosted smoke passes on the live Space.
5. The supported category set above matches the intended shipped corpus.
6. Any corpus changes since the previous release followed the onboarding
   playbook.
7. A known-good rollback commit is identifiable.

## Out of Scope for This Baseline

This go-live baseline does not imply:

- onboarding new categories automatically;
- supporting `.docx` files;
- proving fresh live validation for every category on every update;
- expanding beyond the current MVP boundary.
