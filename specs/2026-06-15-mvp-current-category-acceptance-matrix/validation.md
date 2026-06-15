# Validation

This slice is ready when the roadmap clearly redirects execution toward MVP
acceptance of the currently onboarded categories and explicitly defers
non-blocking coupling work until that acceptance pass is complete.

## Planned Checks

1. `./.venv/bin/python -m ruff check specs/roadmap.md specs/2026-06-15-mvp-current-category-acceptance-matrix --ignore E501`
2. Manual review confirms:
   - the current category set is named explicitly;
   - the acceptance gates align with `docs/category-onboarding-playbook.md`;
   - remaining coupling slices are deferred rather than deleted;
   - `matrix.md` contains category-specific retrieval and grounded-answer smoke queries.

## Expected Evidence

- the roadmap names `mvp-current-category-acceptance-matrix` as the current
  execution focus;
- the roadmap states that remaining coupling slices are post-MVP unless they
  become unblockers;
- the spec bundle captures the minimum retrieval and grounded-answer evidence
  required per category;
- the acceptance matrix is executable without inventing new categories or query
  families.

## Recorded Evidence

- `./.venv/bin/python -m ruff check specs/roadmap.md specs/2026-06-15-mvp-current-category-acceptance-matrix --ignore E501`
  exits cleanly in this repo state.
- The roadmap now records the first live P1 acceptance snapshot from
  `2026-06-15` and names the three immediate blockers:
  `autos-basico-pt-evidence-family-alignment`,
  `eps-pac-asegurabilidad-policy-family-recovery`, and
  `soat-tariff-table-label-recovery`.
- `matrix.md` now records executed statuses for the first five families:
  - `ARL` = `pass`
  - `MOVILIDAD/AUTOS` = `fail`
  - `EPS/PAC` = `fail`
  - `MOVILIDAD/SOAT` = `fragile-pass`
  - `MOVILIDAD/MUEVETE LIBRE` = `pass`
- Live evidence behind those statuses was collected with:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo consulto la liquidación de comisiones de ARL?' --product arl --document-type guide --top-k 5`
  - `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es la normatividad que rige el RUI?' --product arl --document-type faq --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué diferencia hay entre los planes de autos?' --product auto --document-type guide --top-k 5`
  - `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre el plan autos básico PT?' --product auto --document-type guide --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo actualizo el correo para factura Global Web?' --product pac --document-type guide --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product pac --document-type policy --top-k 5`
  - `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product pac --document-type policy --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el SOAT?' --product soat --document-type policy --top-k 5`
  - `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuáles son las tarifas SOAT 2026?' --product soat --document-type guide --top-k 5`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre Muévete Libre?' --product 'muevete libre' --document-type policy --top-k 5`
  - `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre Muévete Libre?' --product 'muevete libre' --top-k 5`
