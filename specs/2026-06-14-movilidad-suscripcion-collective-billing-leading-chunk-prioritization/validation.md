# Validation

This slice is ready when live collective billing retrieval prefers the cleaner
leading `14.6.2` chunk over later fragmentary continuations.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval coverage proves the cleaner leading `14.6.2` chunk is
  preferred.
- Live retrieval stays inside the suscripción document family.
- At least one live collective billing query returns the cleaner `14.6.2`
  chunk ahead of the later fragmentary `14.6.2` chunk.

## Baseline Gap Evidence

- After collective-billing intent alignment, the live query
  `cómo funciona la facturación de pólizas colectivas en movilidad`
  already ranks the correct `14.6.2` subsection first.
- The selected live chunk can still begin with the fragment
  `onciliación.` while earlier `14.6.2` chunks in the same subsection contain
  a cleaner billing explanation lead.
- The remaining gap is therefore within-subsection leading-chunk selection, not
  document family, section lineage, or billing intent alignment.

## Completion Evidence

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'collective_billing'`
  passed after adding focused regressions for exact `14.6.2` lead preference
  and local lexical candidate recovery.
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
  passed.
- Live retrieval for
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'cómo funciona la facturación de pólizas colectivas en movilidad' --product movilidad --document-type policy --top-k 5`
  now returns
  `movilidad__transversales__politicas-de-suscripcion-de-movilidad:v2:0109`
  first, which is the cleaner `14.6.2` billing explanation lead.
- The later fragmentary chunk
  `movilidad__transversales__politicas-de-suscripcion-de-movilidad:v2:0111`
  no longer displaces that cleaner `14.6.2` lead.
- Retrieval remains inside the suscripción document family and still keeps
  collective billing evidence ahead of financing-individual content.
