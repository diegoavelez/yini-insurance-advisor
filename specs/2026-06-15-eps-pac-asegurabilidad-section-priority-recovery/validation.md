# Validation

This slice is ready when the explicit `PAC 60 Más` asegurabilidad query keeps the correct family and also surfaces the direct asegurabilidad sections first.

## Acceptance checks

- A committed spec bundle exists for `eps-pac-asegurabilidad-section-priority-recovery`.
- The term-equivalence file contains one explicit `PAC 60 Más` asegurabilidad expansion rule.
- Focused tests confirm the query appends the intended section anchors and expands the candidate pool.
- Focused tests confirm reranking prefers `GRUPOS ASEGURABLES` over unrelated in-family operational sections.
- Live retrieval for `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` ranks `GRUPOS ASEGURABLES` or direct age/admission chunks first.
- Live grounded answering cites the direct asegurabilidad sections prominently.
- Roadmap and MVP matrix record the outcome accurately.

## Verification commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'pac_asegurabilidad_section or repository_pac_60_mas_asegurabilidad'`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product pac --document-type policy --top-k 5`
- `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product pac --document-type policy --top-k 5`
