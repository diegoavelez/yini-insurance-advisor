# Validation

This slice is ready when explicit utilitarios y pesados coverage queries resolve to the dedicated clausulado family and the guide smoke remains stable.

## Acceptance Checks

- A committed spec bundle exists for `utilitarios-pesados-policy-family-recovery`.
- The term-equivalence file contains a deterministic policy-family routing rule.
- Focused tests confirm the policy-family normalization.
- Live answer for `¿Qué cubre el plan de utilitarios y pesados?` cites `clausulado-plan utilitarios y pesados.pdf`.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'utilitarios_pesados_policy'`
- `./.venv/bin/python -m ruff check tests/test_retrieval.py --ignore E501`
- `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre el plan de utilitarios y pesados?' --product movilidad --document-type policy --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué beneficios tiene el seguro de utilitarios y pesados?' --product movilidad --document-type guide --top-k 5`
