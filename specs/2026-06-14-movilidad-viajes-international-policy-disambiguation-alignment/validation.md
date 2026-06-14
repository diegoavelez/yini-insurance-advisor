# Validation

This slice is ready when explicit viajes policy-variant queries disambiguate to
the correct document family.

## Expected live checks

- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué cubre el clausulado de viaje internacional' --product 'viajes' --document-type policy --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué cubre el clausulado de viaje nacional' --product 'viajes' --document-type policy --top-k 5`

## Validation evidence

- Focused pytest:
  `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'viajes and (international or national or broad_viajes_policy or canonicalizes_viajes_product_alias)'`
  → `6 passed`
- Live retrieval for `viaje internacional` returned only
  `CONDICIONADO SEGURO VIAJE INTERNACIONAL` chunks in the top-5 results.
- Live retrieval for `viaje nacional` returned only
  `CONDICIONADO SEGURO VIAJE NACIONAL` chunks in the top-5 results.
