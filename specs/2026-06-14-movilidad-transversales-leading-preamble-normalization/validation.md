# Validation

This slice is ready when the two choque-simple process guides no longer emit a
leading chunk without section metadata.

## Acceptance Checks

- The new spec bundle exists.
- Focused ingestion coverage proves both guides promote stable root headings.
- Rebuilt chunks for both guides no longer begin with `section = None`.
- The leading chunks preserve meaningful section paths after normalization.

## Baseline Gap Evidence

- `movilidad__transversales__proceso-atencion-choque-simple-v2:v2:0000`
  currently has `section = None` and text `Normatividad vigente`.
- `movilidad__transversales__proceso-recobro-choque-simple-v2:v2:0000`
  currently has `section = None` and contains the opening advisory sentence
  before the first heading.

## Completion Evidence

- Focused ingestion coverage passes with
  `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'choque_simple or suscripcion_headings or leading_preamble or root_heading'`.
- Static verification passes with
  `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`.
- Regenerating the two affected artifacts from cached `data/markdown/*.md`
  now yields:
  - `movilidad__transversales__proceso-atencion-choque-simple-v2` first chunk
    with `section = EN EVENTOS DE CHOQUES` and `none_sections = 0`;
  - `movilidad__transversales__proceso-recobro-choque-simple-v2` first chunk
    with `section = Solo daños materiales`,
    `section_path = ['Servicios de recobro para accidentes', 'Solo daños materiales']`,
    and `none_sections = 0`.
