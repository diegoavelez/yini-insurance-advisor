# Validation

This slice is ready when explicit `Autos Básico PT` guide queries stay inside the intended `Plan Autos Básico Pérdidas Totales` family and any remaining AUTOS comparison gap is documented separately.

## Acceptance checks

- A committed spec bundle exists for `autos-basico-pt-evidence-family-alignment`.
- Repository-loaded term equivalences inject `document_name = Plan Autos Básico Pérdidas Totales` for explicit `Autos Básico PT` guide queries.
- Explicit `Autos Básico PT` coverage queries append narrow coverage recall terms and expand the candidate pool beyond bare `top_k`.
- Generic AUTOS comparison queries do not receive the `Básico PT` family filter.
- Focused retrieval tests pass.
- Live retrieval for `¿Qué cubre el plan autos básico PT?` returns the intended guide family.
- Live grounded answering for `¿Qué cubre el plan autos básico PT?` no longer cites unrelated AUTOS guide families.
- `specs/roadmap.md` and the MVP matrix record the outcome accurately.

## Verification commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'autos_basico_pt or repository_autos_basico_pt'`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el plan autos básico PT?' --product auto --document-type guide --top-k 5`
- `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre el plan autos básico PT?' --product auto --document-type guide --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué diferencia hay entre los planes de autos?' --product auto --document-type guide --top-k 5`
