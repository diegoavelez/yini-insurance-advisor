# Validation

This slice is ready when ARL remuneration-policy chunks no longer repeat their
leading section headings.

## Acceptance Checks

- The new spec bundle exists.
- Focused ingestion coverage proves duplicated heading scaffolds are removed.
- Rebuilt remuneration-policy chunks no longer repeat leading headings such as
  `## Canales para la afiliación a ARL SURA`.
- Live remuneration-policy retrieval still returns the policy family with a
  cleaner chunk surface.

## Baseline Gap Evidence

- Current chunk `arl__politica-de-remuneracion-canal-externo-v4:v2:0001`
  repeats `## Canales para la afiliación a ARL SURA`.
- Current chunk `arl__politica-de-remuneracion-canal-externo-v4:v2:0021`
  repeats `## Clientes nuevos (venta) para el Canal Externo`.
- Current chunk `arl__politica-de-remuneracion-canal-externo-v4:v2:0024`
  repeats `## Por cambio de intermediario`.

## Completion Evidence

- Added chunk-surface dedup helpers in `rag/ingestion.py` so section-path
  prefixes do not repeat the same heading scaffold at the top of the chunk and
  repeated section headings already covered by the prefix are dropped from the
  rendered chunk text.
- Added focused ingestion tests in `tests/test_ingestion.py` covering:
  duplicated leading section headings, the remuneration-policy heading surface,
  and repeated section-heading echoes inside the chunk body.
- Verified focused checks:
  - `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'remuneracion or heading_scaffold or repeated_section_heading or arl_commissions or arl_rui'`
  - `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- Rebuilt the remuneration-policy chunk bundle and regenerated/reindexed
  `arl__politica-de-remuneracion-canal-externo-v4` embeddings into Qdrant
  Cloud.
- Live retrieval now returns deduplicated chunk surfaces for the known affected
  sections:
  - `retrieve-chunks --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 3`
    returns `arl__politica-de-remuneracion-canal-externo-v4:v2:0001` with a
    single `## Canales para la afiliación a ARL SURA`.
  - `retrieve-chunks --query 'clientes nuevos venta canal externo arl' --product arl --document-type policy --top-k 3`
    returns `arl__politica-de-remuneracion-canal-externo-v4:v2:0021` without
    repeating `## Clientes nuevos (venta) para el Canal Externo`.
  - `retrieve-chunks --query 'cambio de intermediario arl remuneración' --product arl --document-type policy --top-k 3`
    returns `arl__politica-de-remuneracion-canal-externo-v4:v2:0024` without
    repeating `## Por cambio de intermediario`.
- Residual gap: chunk `v2:0021` still exposes a parent heading
  `## Pago de comisiones por Atracción` after the child heading; this no longer
  duplicates the child section, but it remains a narrower hierarchy-compaction
  follow-up and is not required to close this slice.
