# Validation

This slice is ready when the bicicletas/patinetas coverage smoke query cites the clausulado family and the deductible path remains stable.

## Acceptance checks

- A committed spec bundle exists for `bicicletas-patinetas-coverage-policy-family-recovery`.
- The term-equivalence file contains a deterministic bicicletas/patinetas coverage `document_name` rule.
- Focused tests confirm explicit coverage queries normalize to `SEGURO DE BICICLETA`.
- Live retrieval for `¿Qué cubre el seguro para bicicletas y patinetas?` returns the clausulado family.
- Live grounded answering cites `clausulado-bicis y patinetas.pdf` instead of `politicas de suscripcion de movilidad.pdf`.
- Live retrieval for `¿Cuál es el deducible del seguro de bicicletas y patinetas?` still prioritizes `pv bicis y patinetas v2.pdf`.
- Roadmap and acceptance matrix record the result accurately.

## Verification commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'bicicletas_patinetas_coverage or repository_bicicletas_patinetas_coverage'`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el seguro para bicicletas y patinetas?' --product movilidad --document-type policy --top-k 5`
- `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre el seguro para bicicletas y patinetas?' --product movilidad --document-type policy --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cuál es el deducible del seguro de bicicletas y patinetas?' --product movilidad --document-type guide --top-k 5`
