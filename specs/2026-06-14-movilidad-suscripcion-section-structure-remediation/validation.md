# Validation

This slice is ready when the suscripción policy surface exposes semantic
section structure and live retrieval no longer relies on generic `Page N`
chunks or broken fallback fragments.

## Acceptance Checks

- The new spec bundle exists.
- The baseline evidence records that the document family is correct but the
  extracted structure is weak.
- The cleaned markdown head is materially less noisy.
- Retrieved chunk sections become more semantic than `Page N`.
- Live retrieval remains inside the suscripción document family.

## Baseline Gap Evidence

- The baseline onboarding completed only after reducing the operational Docling
  timeout to trigger PDFium fallback on the 64-page source PDF.
- The cleaned markdown head still contains page boilerplate and table-of-
  contents noise.
- The first live retrieval results include generic or weak chunks such as:
  - `Page 9` with `Terceros y Asistencia.`
  - `Page 43` with a residual fragment
  - `Page 11` with `iarios`
- The gap is therefore extraction/section-structure quality, not
  cross-document retrieval leakage.

## Completion Evidence

- Focused normalization coverage now passes in:
  - `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
  - `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- The suscripción cleaned markdown head now starts with:
  - `# politicas de suscripcion de movilidad`
  - `Versión 6 5 – abril 202 6`
  - `## 1. DEFINICIÓN DE RIESGO ESTÁNDAR`
  instead of `Page N`, `Volver al inicio`, and table-of-contents fragments.
- Regenerated chunk sections are now semantic policy headings such as:
  - `1. DEFINICIÓN DE RIESGO ESTÁNDAR`
  - `2. DEFINICIÓN DE TIPO DE SERVICIO`
  - `13. PROCEDIMIENTOS`
  - `14.1. Cotización de Pólizas Colectivas`
- Live retrieval for:
  - `cuáles son las políticas de suscripción de movilidad`
  - `qué reglas de suscripción aplican en movilidad`
  remains inside the suscripción policy family and no longer returns generic
  `Page N` sections or broken fragments like `iarios`.
- The remaining suscripción issue is now narrower: section-heading-only chunks
  can still outrank richer body chunks for broad policy queries, so the next
  slice is evidence prioritization rather than additional structure cleanup.
