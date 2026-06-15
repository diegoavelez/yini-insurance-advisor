# Validation

This slice is ready when the broad AUTOS comparison smoke query promotes `DIFERENCIALES SURA` ahead of unrelated AUTOS guide families without regressing the explicit `Autos Básico PT` path.

## Acceptance checks

- A committed spec bundle exists for `autos-comparison-primary-guide-ranking-recovery`.
- The repository term-equivalence file contains one broad AUTOS comparison expansion rule.
- Focused tests confirm the broad query appends comparison anchors and expands the candidate pool.
- Focused tests confirm broad AUTOS comparison ranking prefers `DIFERENCIALES SURA`.
- Live retrieval for `¿Qué diferencia hay entre los planes de autos?` ranks `diferenciales planes autos.pdf` first.
- Live retrieval for `¿Qué cubre el plan autos básico PT?` remains anchored to `generalidades plan autos basico pt v2.pdf`.
- Roadmap and MVP matrix record the outcome accurately.

## Verification commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'broad_autos_comparison or autos_basico_pt'`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué diferencia hay entre los planes de autos?' --product auto --document-type guide --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el plan autos básico PT?' --product auto --document-type guide --top-k 5`
