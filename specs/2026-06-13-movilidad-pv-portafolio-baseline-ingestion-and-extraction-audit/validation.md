# Validation

Executed checks for this slice:

1. `make batch-ingest BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/TRANSVERSALES/pv *.pdf' BATCH_OVERWRITE=false`
2. Verified generated artifacts for:
   - `movilidad__transversales__pv-planes-movilidad-v1`
   - `movilidad__transversales__pv-portafolio-movilidad-v2`
3. Inspected:
   - `data/processed/movilidad__transversales__pv-planes-movilidad-v1.cleaned.md`
   - `data/processed/movilidad__transversales__pv-portafolio-movilidad-v2.cleaned.md`
   - corresponding `data/processed/chunks/*.chunks.json`

Observed outcome:

- Both `PV` documents ingest successfully under the current Docling-first flow.
- Title promotion is acceptable and stable for both documents:
  `PROPUESTA DE VALOR MOVILIDAD`.
- Extraction quality is mixed but usable enough to justify a dedicated
  remediation slice before embeddings/indexing:
  - repeated structural headings remain in chunk text;
  - commercial labels such as `PLANES QUE APLICA` and repeated portfolio
    fragments produce many small, repetitive chunks;
  - `pv portafolio movilidad v2` currently generates `119` chunks and
    `pv planes movilidad v1` generates `104`, which is high for a two-document
    commercial cohort.
- The next narrow slice should target `PV` structure normalization and chunk
  deduplication before live retrieval alignment work.
