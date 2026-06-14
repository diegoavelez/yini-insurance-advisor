# Validation

This slice is ready when the current four-document `ARL` cohort is proven live
through Qdrant indexing plus retrieval and answer validation.

## Acceptance Checks

- The new spec bundle exists.
- `data/processed/qdrant-indexing-manifest.jsonl` contains successful entries
  for the current four `ARL` source PDFs.
- Live retrieval succeeds for representative `guide`, `faq`, and `policy`
  queries under `product=arl`.
- A live `answer-query` call succeeds for a representative `ARL/RUI` question.
- The roadmap records both closure of this operational slice and the next
  narrow `ARL` corrective gap.

## Baseline Gap Evidence

- Before this slice, `data/processed/embeddings/` already contained the four
  current `ARL` embedding artifacts.
- Before this slice, `data/processed/qdrant-indexing-manifest.jsonl` contained
  no `arl__*` entries.

## Completion Evidence

- Live indexing succeeded with:
  `./.venv/bin/python -m rag.ingestion index-embeddings --embedding-dir data/processed/embeddings --manifest-path data/processed/qdrant-indexing-manifest.jsonl --glob 'arl__*.embeddings.json' --fail-fast true`
- The indexing manifest now contains successful entries for:
  - `arl__instructivos-actualizacion-cuenta-bancaria-v2`
  - `arl__instructivos-consulta-de-comisiones-arl-sura-v2`
  - `arl__politica-de-remuneracion-canal-externo-v4`
  - `arl__preguntas-frecuentes-registro-unico-de-intermediacion-rui`
- Live retrieval succeeded with:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo actualizo la cuenta bancaria para pago de comisiones ARL?' --product arl --document-type guide --top-k 3`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cuál es la normatividad que rige el registro único de intermediarios?' --product arl --document-type faq --top-k 3`
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 3`
- The guide query returned `Actualización de cuenta bancaria para pago de comisiones ARL SURA` first.
- The FAQ query returned the `preguntas frecuentes registro unico de intermediacion - rui` document family first, including the chunk that enumerates `Ley 1562 de 2012`, `Decreto 1117 de 2016`, and `Resolución 0136 de 2024`.
- The policy query returned the `Canal Externo ARL V1 Esquema remuneración y políticas que lo complementan` policy family first.
- Live grounded-answer validation succeeded with:
  `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es la normatividad que rige el RUI?' --product arl --document-type faq --top-k 5`
- The answer completed with `supported = true`, `confidence = high`, and cited the indexed `ARL/preguntas frecuentes registro unico de intermediacion - rui.pdf` corpus.

## Follow-on Gap

- Live `ARL/RUI` validation also exposed a narrow quality gap: the current FAQ
  structure still promotes noisy heading candidates such as the Vimeo label and
  `MINISTERIODELTRABAJO`, and answer citations can include lateral numbered
  questions beyond the exact normativity evidence.
- The next narrow corrective slice is therefore
  `arl-rui-faq-heading-and-citation-precision`.
