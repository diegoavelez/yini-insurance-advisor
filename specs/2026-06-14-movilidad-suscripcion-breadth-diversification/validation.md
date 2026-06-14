# Validation

This slice is ready when broad suscripción policy queries surface contentful
evidence from distinct policy sections before repeating the same subsection.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval coverage proves repeated suscripción subsection chunks are
  diversified deterministically.
- Live retrieval stays inside the suscripción document family.
- At least one broad suscripción live query surfaces more than one distinct
  policy section in the first results.

## Baseline Gap Evidence

- After the heading-stub remediation, live retrieval for
  `cuáles son las políticas de suscripción de movilidad`
  no longer returned bare heading stubs first.
- The first live results still concentrated on repeated contentful chunks from
  `14.1. Cotización de Pólizas Colectivas` before surfacing broader distinct
  policy sections.
- The remaining gap is therefore breadth diversification within the same
  suscripción family.

## Completion Evidence

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q` passed after the
  suscripción breadth-diversification changes.
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
  passed.
- Live retrieval for
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'cuáles son las políticas de suscripción de movilidad' --product movilidad --document-type policy --top-k 5`
  now surfaces distinct contentful sections in the first results, including:
  - `14.1. Cotización de Pólizas Colectivas`
  - `2. DEFINICIÓN DE TIPO DE SERVICIO`
  - `4.3. Traslado entre planes`
  - `14.7. Opciones de Intervención de Pólizas Colectivas con Aumento en su Siniestralidad`
- The previous duplicate-subsection pattern no longer dominates the top-k.
- A narrower follow-up gap remains in section labeling: under
  `14. PÓLIZAS COLECTIVAS`, some child headings still surface with inconsistent
  numbering such as `2.1` and `2.2`, indicating a lineage-normalization issue
  rather than a ranking issue.
