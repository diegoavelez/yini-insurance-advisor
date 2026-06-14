# Validation

This slice is ready when ARL remuneration-policy retrieval no longer surfaces
standalone heading-only overlap chunks.

## Acceptance Checks

- The new spec bundle exists.
- Focused ingestion coverage proves heading-only overlap chunks are skipped.
- Rebuilt ARL remuneration-policy chunks no longer contain a standalone chunk
  composed only of `## Clientes nuevos (venta) para el Canal Externo` and
  `## Pago de comisiones por Atracción`.
- Live remuneration-policy retrieval still succeeds and surfaces richer policy
  chunks for the affected section.

## Baseline Gap Evidence

- Current chunk `arl__politica-de-remuneracion-canal-externo-v4:v2:0021`
  contains only parent/child heading scaffolds and no substantive policy text.

## Completion Evidence

- Added a chunk-surface guard in `rag/ingestion.py` so chunk emission now skips
  standalone overlaps composed only of markdown headings and blank lines.
- Added focused ingestion coverage in `tests/test_ingestion.py` proving
  heading-only overlap chunks are skipped while substantive `Section A` and
  `Section B` chunks remain.
- Verified focused checks:
  - `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'heading_only_overlap or heading_scaffold or repeated_section_heading or remuneracion'`
  - `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- Rebuilt the remuneration-policy chunk bundle, regenerated embeddings, and
  reindexed `arl__politica-de-remuneracion-canal-externo-v4` into Qdrant
  Cloud.
- The rebuilt chunk bundle now preserves only substantive `Clientes nuevos`
  chunks (`v2:0008` and `v2:0009`); the previous standalone heading-only
  overlap chunk for that section is no longer emitted.
- Live retrieval confirmation:
  - `retrieve-chunks --query 'clientes nuevos venta canal externo arl' --product arl --document-type policy --top-k 5`
    now surfaces substantive `Clientes nuevos (venta) para el Canal Externo`
    chunks instead of a heading-only scaffold chunk.
  - `retrieve-chunks --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`
    still succeeds after reindexing and keeps the remuneration policy
    retrievable in Qdrant Cloud.
