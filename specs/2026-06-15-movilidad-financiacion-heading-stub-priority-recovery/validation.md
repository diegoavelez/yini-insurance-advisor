# Validation

This slice is ready when explicit financing-guide prompts prefer contentful
procedural chunks over bare heading stubs inside the financing guide family.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval coverage proves the `Procedimientos:` stub is demoted below
  richer `Paso a paso` or `Notas Importantes` chunks in the same guide family.
- Live retrieval for
  `¿Cómo funciona la financiación de pólizas individuales?`
  returns a contentful financing-guide chunk first.
- Live grounded answering stays inside
  `MOVILIDAD/TRANSVERSALES/instructivo financiacion de polizas v1.pdf`.

## Baseline Gap Evidence

- `MOVILIDAD/FINANCIACION` already stayed inside the correct guide family, but
  top retrieval still started with a heading-only `Procedimientos:` chunk.
- The category therefore remained `fragile-pass` in the acceptance matrix due
  intra-family evidence quality, not family leakage.

## Completion Evidence

- Focused retrieval coverage passes with:
  `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'financing_guide'`
- `./.venv/bin/python -m ruff check rag/evidence_selection.py tests/test_retrieval.py --ignore E501`
  passes.
- Live validation passes with:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo funciona la financiación de pólizas individuales?' --product movilidad --top-k 5`
  - `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cómo funciona la financiación de pólizas individuales?' --product movilidad --top-k 5`
- The live top result is now chunk
  `movilidad__transversales__instructivo-financiacion-de-polizas-v1:v2:0004`
  at section `Paso a paso`, ahead of the former `Procedimientos:` stub.
- The grounded answer remains inside
  `MOVILIDAD/TRANSVERSALES/instructivo financiacion de polizas v1.pdf` with
  `confidence=high`.
- Residual OCR compaction may still appear in lower-ranked chunks, but it no
  longer blocks MVP acceptance and is captured in the acceptance matrix note.
