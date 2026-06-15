# Validation

This slice is ready when the PAC `60 Más` asegurabilidad query no longer drifts
into the clausulado family and the MVP matrix can promote the PAC row from
`fail`.

## Planned checks

1. `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'pac_asegurabilidad_document_name or repository_pac_asegurabilidad'`
2. `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product pac --document-type policy --top-k 5`
3. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product pac --document-type policy --top-k 5`

## Expected evidence

- the repository term-equivalence rules normalize the PAC `60 Más`
  asegurabilidad query to `document_name="Plan Complementario 60 más"`;
- live retrieval ranks the `politicas asegurabilidad pac 60 mas.pdf` family
  ahead of `clausulado pac 60 mas sura v1.pdf`;
- live grounded answering cites only the intended asegurabilidad family or a
  tightly bounded subset of that family.

## Recorded evidence

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'pac_asegurabilidad_document_name or repository_pac_60_mas'` passed.
- Repository-rule normalization now behaves as intended:
  - `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` normalizes to
    `document_name="Plan Complementario 60 más"`.
  - `¿Qué cubre el PAC 60 Más?` still normalizes to
    `document_name="Es tiempo devIvIr mas historias."`.
- Live retrieval now stays inside the intended PAC `60 Más` asegurabilidad
  family:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product pac --document-type policy --top-k 5`
  - returned only `EPS/PLAN COMPLEMENTARIO PAC/politicas asegurabilidad pac 60 mas.pdf`
    chunks.
- Live grounded answering now stays in the same family:
  - `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product pac --document-type policy --top-k 5`
  - completed with `supported=true`, `confidence=high`, and cited only
    `EPS/PLAN COMPLEMENTARIO PAC/politicas asegurabilidad pac 60 mas.pdf`.
- Remaining weakness after the family recovery:
  - top in-family chunks still include broader sections such as
    `CONGELACIONES` and `REACTIVACIÓN...` before the more directly relevant
    `GRUPOS ASEGURABLES` section, so the PAC row should be promoted from
    `fail` to `fragile-pass`, not directly to `pass`.
