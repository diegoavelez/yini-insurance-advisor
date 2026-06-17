# Evaluation Report

## Purpose

This report is the current `Phase 15` baseline evaluation artifact for the
MVP. It summarizes the evaluation assets already committed in the repository,
the deterministic baseline checks that were executed locally, and the accepted
category families currently protected by the MVP acceptance smoke asset.

This report is intentionally conservative:

- it documents deterministic local evaluation evidence;
- it documents the committed MVP acceptance smoke coverage surface;
- it does **not** claim fresh live Qdrant or Groq validation beyond what is
  already separately documented in `specs/roadmap.md`.

## Scope

The baseline covers three surfaces:

1. the deterministic local evaluation set under `data/eval/`;
2. the hosted-like citation smoke over the current evaluation assets;
3. the committed MVP acceptance smoke dataset for the currently accepted
   category set.

The baseline does not cover:

- fresh live external execution against Qdrant Cloud or Groq;
- `.docx` forms, which are excluded from the MVP corpus and answer surface;
- new retrieval-quality judgments beyond the currently committed smoke
  expectations.

## Evaluation Asset Inventory

### Deterministic local evaluation assets

| Artifact | Version | Count | Purpose |
| --- | --- | ---: | --- |
| `data/eval/questions.json` | `2026-06-08-target-30-spanish-v1` | 30 questions | curated Spanish evaluation prompts |
| `data/eval/golden-behaviors.json` | `2026-05-19-golden-behaviors-v1` | 30 expectations | expected guardrail/scope behavior |
| `data/eval/retrieval-expectations.json` | `2026-05-20-retrieval-expectations-v1` | 30 expectations | retrieval expectation alignment set |
| `data/eval/citation-expectations.json` | `2026-05-20-citation-expectations-v1` | 30 expectations | citation posture alignment set |

### MVP acceptance smoke asset

| Artifact | Version | Count | Purpose |
| --- | --- | ---: | --- |
| `data/eval/mvp-acceptance-smokes.json` | `2026-06-18-current-category-acceptance-v1` | 13 cases | deterministic protection for the currently accepted category set |

## Baseline Results

### Deterministic local evaluation runner

Executed baseline:

- runner: `core.evaluation_runner.run_local_evaluation()`
- run id:
  `local-eval:2026-06-08-target-30-spanish-v1:2026-05-19-golden-behaviors-v1:2026-05-20-retrieval-expectations-v1:2026-05-20-citation-expectations-v1`
- total questions: `30`
- result: `30 matched`, `0 mismatched`

Question-category composition of the current local evaluation set:

- `grounded_qa`: `6`
- `unsupported_query`: `6`
- `prompt_injection`: `6`
- `citation_guardrail`: `6`
- `confidence_guardrail`: `6`

Interpretation:

- the current deterministic local runner still aligns exactly with the
  committed golden-behavior expectation set;
- this proves the current guardrail/scope expectation surface has not drifted
  relative to the curated local evaluation fixtures;
- it does not by itself prove fresh retrieval quality over the live external
  corpus.

### Hosted-like citation smoke

Executed baseline:

- runner: `core.evaluation_runner.run_hosted_citation_regression_smoke()`
- result:
  - `question_count = 30`
  - `all_questions_covered = True`
  - expectation counts:
    - `citations_required = 6`
    - `no_citations_expected = 12`
    - `guardrail_citation_posture = 12`

Interpretation:

- the current citation-expectation set still covers the full local evaluation
  question set;
- the hosted-like citation smoke remains callable and aligned with the current
  curated assets.

## MVP Acceptance Smoke Coverage

The committed MVP acceptance smoke asset protects the currently accepted corpus
with `13` deterministic category-family cases.

### Protected category families

| Category family | Retrieval evidence family | Grounded-answer evidence family |
| --- | --- | --- |
| `ARL` | `instructivos consulta de comisiones arl sura v2.pdf` | `preguntas frecuentes registro unico de intermediacion - rui.pdf` |
| `MOVILIDAD/AUTOS` | `diferenciales planes autos.pdf` | `generalidades plan autos basico pt v2.pdf` |
| `EPS/PAC` | `instructivo actualizacion correo para factura global web v2.pdf` | `politicas asegurabilidad pac 60 mas.pdf` |
| `MOVILIDAD/SOAT` | `clausulado soat.pdf` | `tarifas soat 2026.pdf` |
| `MOVILIDAD/MUEVETE LIBRE` | `clausulado muevete libre v2.pdf` | `clausulado muevete libre v2.pdf` |
| `MOVILIDAD/MOTOS` | `comparativo motos.pdf` | `clausulado-plan motos.pdf` |
| `MOVILIDAD/BICICLETAS Y PATINETAS` | `pv bicis y patinetas v2.pdf` | `clausulado-bicis y patinetas.pdf` |
| `MOVILIDAD/VIAJES` | `clausulado viaje nacional v1.pdf` | `clausulado viaje internacional v1.pdf` |
| `MOVILIDAD/UTILITARIO Y PESADOS` | `ayudaventas utilitarios y pesados v2.pdf` | `clausulado-plan utilitarios y pesados.pdf` |
| `MOVILIDAD/TRANSVERSALES/choque simple` | `como tomar fotos choque simple v2.pdf` | `proceso atencion choque simple v2.pdf` and `circular choque simple.pdf` |
| `MOVILIDAD/PV` | `pv planes movilidad v1.pdf` and `pv portafolio movilidad v2.pdf` | `pv planes movilidad v1.pdf` and `pv portafolio movilidad v2.pdf` |
| `MOVILIDAD/FINANCIACION` | `instructivo financiacion de polizas v1.pdf` | `instructivo financiacion de polizas v1.pdf` |
| `MOVILIDAD/SUSCRIPCION` | `politicas de suscripcion de movilidad.pdf` | `politicas de suscripcion de movilidad.pdf` |

Interpretation:

- this smoke asset protects the currently accepted category set against
  evidence-family drift;
- it is deterministic because the runner takes injected retrieval and answer
  callables;
- it complements, but does not replace, the earlier live category-acceptance
  evidence already documented in `specs/roadmap.md`.

## MVP Boundaries Relevant to Evaluation

- ingestion is intentionally PDF-only;
- `.docx` Word forms are excluded from the MVP corpus;
- `.docx` files are not expected retrieval evidence and are not valid answer
  artifacts for this MVP report;
- the current acceptance smoke focuses on evidence-family alignment, not on
  free-form answer style grading.

## Rerun Commands

Deterministic local evaluation snapshot:

```bash
./.venv/bin/python - <<'PY'
from collections import Counter
from core.evaluation_runner import run_local_evaluation
result = run_local_evaluation()
print(result.run_id)
print(Counter(item.status for item in result.results))
PY
```

Hosted-like citation smoke:

```bash
./.venv/bin/python - <<'PY'
from core.evaluation_runner import run_hosted_citation_regression_smoke
print(run_hosted_citation_regression_smoke())
PY
```

Focused regression coverage:

```bash
./.venv/bin/python -m pytest tests/test_evaluation_dataset.py tests/test_evaluation_runner.py tests/test_smoke.py -q
```

## Report Limits

This baseline report should be read as:

- a truthful summary of the current deterministic evaluation posture;
- a durable index of the accepted category families protected by smoke assets;
- a handoff document for future MVP review and final cleanup work.

It should not be read as:

- proof that every live external dependency was rerun at the moment this report
  was updated;
- a replacement for targeted live retrieval or deployment validation when the
  corpus or runtime changes materially.
