# Validation

This slice is ready when the `ARL/RUI` FAQ produces semantic question sections
and live citations no longer depend on noisy portal headings.

## Acceptance Checks

- The new spec bundle exists.
- Focused ingestion coverage proves numbered FAQ questions become semantic
  headings.
- Rebuilt FAQ chunks no longer use `Grabación: ...` or `MINISTERIODELTRABAJO`
  as the primary early section labels.
- Live retrieval for the RUI normativity query returns the exact FAQ question
  section first.
- Live grounded-answer validation cites the cleaned FAQ structure without using
  noisy portal headings as its primary evidence anchor.

## Baseline Gap Evidence

- The current FAQ chunk bundle uses `Grabación: https:/ /player.vimeo.com/...`
  as the first section label.
- The next early FAQ chunks use `MINISTERIODELTRABAJO` as their section label.
- The current cleaned markdown contains a portal/status interruption with
  `iRegistro Unico de Intermediarios`, `MINISTERIODELTRABAJO`, and a large
  table before later numbered questions resume.

## Completion Evidence

- Focused ingestion and grounded-answer coverage passes with:
  `./.venv/bin/python -m pytest tests/test_ingestion.py tests/test_grounded_answer_generation.py -q -k 'arl_rui or rui or financing_evidence or typed_response_with_citations or root_heading'`
- Static verification passes with:
  `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py tests/test_grounded_answer_generation.py`
- Rebuilding the FAQ artifact from cached markdown now yields semantic question
  sections such as:
  - `1. ¿Cuál es la normatividad que rige el registro único de intermediarios?`
  - `2. Teniendo en cuenta que uno de los cambios de la resolución 0136 de 2024 es la vigencia del RUI. ¿Cómo puedo saber si mi RUI se vence en 3 o 4 años?`
- The rebuilt chunk bundle no longer uses `Grabación: ...` or
  `MINISTERIODELTRABAJO` as the early FAQ section labels.
- Live indexing of the refreshed FAQ embedding artifact succeeds with:
  `./.venv/bin/python -m rag.ingestion index-embeddings --embedding-dir data/processed/embeddings --manifest-path data/processed/qdrant-indexing-manifest.jsonl --glob 'arl__preguntas-frecuentes-registro-unico-de-intermediacion-rui.embeddings.json' --fail-fast true`
- Live retrieval now returns the exact normativity question section first with:
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cuál es la normatividad que rige el RUI?' --product arl --document-type faq --top-k 5`
- Live grounded-answer validation now returns one precise citation and one
  documentary-basis entry, both anchored on the exact normativity question,
  with:
  `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es la normatividad que rige el RUI?' --product arl --document-type faq --top-k 5`
