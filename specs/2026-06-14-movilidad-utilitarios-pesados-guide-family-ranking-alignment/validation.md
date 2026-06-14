# Validation

> Superseded in canonical classification by
> `specs/2026-06-14-movilidad-utilitarios-pesados-category-reclassification-remediation/validation.md`.
> The guide-family rule remains valid, but live validation should use the
> dedicated category/product contract.

This slice is ready when explicit `utilitarios y pesados` guide-intent queries
stay within the `Seguro de Autos Utilitarios y Pesados` document family by
default, while policy retrieval remains unchanged.

## Acceptance Checks

- The new spec bundle exists.
- `ops/term-equivalences.json` includes a cohort guide-specific
  `document_name` query filter rule.
- Focused retrieval tests prove the normalized query carries the cohort guide
  `document_name` filter.
- Focused retrieval tests prove local lexical candidates from generic
  movilidad guides are excluded for this narrow intent.
- The roadmap records the baseline cohort as complete and the new corrective
  slice as remaining work.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
- `./.venv/bin/python -m ruff check tests/test_retrieval.py`
- `./.venv/bin/python -m json.tool ops/term-equivalences.json`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué beneficios o asistencias tienen los utilitarios y pesados' --product movilidad --document-type guide --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué cubre el plan de utilitarios y pesados' --product movilidad --document-type policy --top-k 5`

## Execution Notes

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q` passed locally.
- `./.venv/bin/python -m ruff check tests/test_retrieval.py` passed locally.
- `./.venv/bin/python -m json.tool ops/term-equivalences.json` passed locally.
- Live rerun of `qué beneficios o asistencias tienen los utilitarios y pesados`
  returned only `Seguro de Autos Utilitarios y Pesados` guide chunks.
- Live rerun of `qué cubre el plan de utilitarios y pesados` remained within
  the expected `SEGURO DE AUTOS PLAN UTILITARIOS Y PESADOS` policy family.

## Expected Outcome

- Queries like `qué beneficios o asistencias tienen los utilitarios y pesados`
  default to `Seguro de Autos Utilitarios y Pesados`.
- Generic movilidad PV chunks no longer crowd the top results for this narrow
  guide intent.
- The slice stops before broader taxonomy or reranker redesign.
