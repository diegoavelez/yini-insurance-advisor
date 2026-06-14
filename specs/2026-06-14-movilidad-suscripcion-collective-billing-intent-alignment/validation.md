# Validation

This slice is ready when explicit collective billing prompts prefer the
`14.6.*` suscripción sections over adjacent financing-individual content.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval coverage proves collective billing intent prefers `14.6.*`
  sections.
- Live retrieval stays inside the suscripción document family.
- At least one live collective billing query returns a `14.6.*` section ahead
  of `13.11. Financiación de Pólizas Individuales`.

## Baseline Gap Evidence

- After subsection-lineage normalization, live retrieval for
  `cómo funciona la facturación de pólizas colectivas en movilidad`
  already returns the corrected label
  `14.6.2. Facturación (cobro) agrupada con devolución por asegurado`.
- The same live query can still rank
  `13.11. Financiación de Pólizas Individuales`
  ahead of that collective billing result.
- The remaining gap is therefore intent alignment, not family scoping, section
  lineage, or breadth diversification.

## Completion Evidence

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'collective_billing_intent or suscripcion'`
  passed after the collective billing intent-alignment change.
- `./.venv/bin/python -m pytest tests/test_retrieval.py -q` passed.
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
  passed.
- Live retrieval for
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'cómo funciona la facturación de pólizas colectivas en movilidad' --product movilidad --document-type policy --top-k 5`
  now ranks
  `14.6.2. Facturación (cobro) agrupada con devolución por asegurado`
  ahead of
  `13.11. Financiación de Pólizas Individuales`.
- Retrieval remains inside the suscripción document family.
- The narrower within-subsection follow-up documented here was subsequently
  closed by the leading-chunk prioritization slice, which now returns the
  cleaner `14.6.2` lead chunk ahead of later fragmentary continuations.
