# Validation

This slice is ready when broad suscripción policy queries return richer body
evidence ahead of bare section-heading stubs from the same document family.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval coverage proves heading-only suscripción chunks are
  demoted relative to richer body chunks in the same family.
- Live retrieval stays inside the suscripción document family.
- At least one broad suscripción policy query now returns contentful evidence
  ahead of section-heading-only chunks.

## Baseline Gap Evidence

- After section-structure remediation, live retrieval for
  `cuáles son las políticas de suscripción de movilidad`
  still ranked heading-only chunks such as:
  - `13. PROCEDIMIENTOS`
  - `14. PÓLIZAS COLECTIVAS`
  ahead of richer body evidence.
- The remaining gap is therefore evidence prioritization inside the suscripción
  family, not family leakage or page-structure noise.

## Completion Evidence

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q` passed after the
  suscripción reranking changes.
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
  passed.
- Live retrieval for
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'cuáles son las políticas de suscripción de movilidad' --product movilidad --document-type policy --top-k 5`
  now returns contentful chunks ahead of bare heading stubs, including:
  - `14.1. Cotización de Pólizas Colectivas`
  - `2. DEFINICIÓN DE TIPO DE SERVICIO`
  - `4.3. Traslado entre planes`
  - `14.7. Opciones de Intervención de Pólizas Colectivas con Aumento en su Siniestralidad`
- The heading-only stub pattern no longer occupies the live top-k for this
  broad suscripción query.
- A narrower follow-up gap remains: broad suscripción prompts can still
  over-concentrate on multiple chunks from the same subsection before
  diversifying across distinct policy sections.
