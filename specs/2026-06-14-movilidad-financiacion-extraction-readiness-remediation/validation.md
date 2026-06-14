# Validation

This slice is ready when `instructivo financiacion de polizas v1.pdf` has a
usable cleaned-markdown and chunk surface, and financing retrieval no longer
depends on unrelated `PV` chunks because of extraction collapse.

## Acceptance Checks

- The new spec bundle exists.
- The failed baseline artifact evidence is recorded.
- A recovered cleaned-markdown surface exists and is materially richer than
  `sura`.
- Regenerated chunks are semantically meaningful.
- At least one financing-oriented retrieval query returns financing-document
  evidence.

## Baseline Failure Evidence

- `data/processed/movilidad__transversales__instructivo-financiacion-de-polizas-v1.cleaned.md` currently equals `sura`.
- `data/processed/chunks/movilidad__transversales__instructivo-financiacion-de-polizas-v1.chunks.json` currently has `chunk_count = 1`.
- Live retrieval for:
  - `cómo funciona la financiación de pólizas en movilidad`
  - `qué opciones de financiación hay para la póliza`
  returned unrelated `PROPUESTA DE VALOR MOVILIDAD` chunks instead of the financing guide.

## Verification Commands

- `sed -n '1,120p' data/processed/movilidad__transversales__instructivo-financiacion-de-polizas-v1.cleaned.md`
- `python - <<'PY' ... inspect chunk bundle ... PY`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'cómo funciona la financiación de pólizas en movilidad' --product movilidad --document-type guide --top-k 5`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query 'qué opciones de financiación hay para la póliza' --product movilidad --document-type guide --top-k 5`

## Execution Notes

- Focused ingestion tests passed after adding the Docling OCR retry.
- Reingestion now produces:
  - `document_name = Manual Procedimiento Financiacion de polizas individuales`
  - `chunk_count = 8`
  - usable procedural sections such as `Cotizacion y expedicion de poliza nueva`,
    `Notas Importantes:`, and `Paso a paso`
- Live retrieval now surfaces financing-guide chunks, proving the extraction
  collapse is fixed.
- A separate ranking/scope issue still remains because `PV` financing mentions
  can outrank the financing guide for explicit financing queries; that issue is
  intentionally tracked as a separate follow-on slice.
