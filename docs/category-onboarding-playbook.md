# Category Onboarding Playbook

This document defines the operator workflow for onboarding a new corpus
category into the local RAG pipeline.

It is based on the corrective experience from:

- `MOVILIDAD/AUTOS`
- `MOVILIDAD/BICICLETAS Y PATINETAS`

The goal is to keep future category onboarding:

- incremental;
- traceable;
- reproducible;
- easy to diagnose when retrieval quality is weak.

## 1. Outcome

A category is considered onboarded only when all of the following are true:

1. PDFs exist under `data/raw/` with stable taxonomy-preserving paths.
2. ingestion artifacts are generated successfully;
3. chunk artifacts are semantically inspectable;
4. embeddings are generated successfully;
5. embeddings are indexed into Qdrant;
6. at least one real retrieval query returns relevant category evidence;
7. at least one real grounded answer cites the intended category documents;
8. any category-specific corrective gaps are captured in dated specs.

Do not treat "ingestion completed" as equivalent to "category is ready".

## 2. Foldering Rule

Preserve the business taxonomy in `data/raw/`.

Example:

```text
data/raw/
  MOVILIDAD/
    AUTOS/
      ayudaventas autos v2.pdf
      diferenciales planes autos.pdf
    BICICLETAS Y PATINETAS/
      ayudaventas bicis y patinetas v2.pdf
      pv bicis y patinetas v2.pdf
```

Why this is the default:

- `source_pdf_relative_path` remains meaningful;
- deterministic `source_pdf_id` generation keeps the category encoded;
- path-derived metadata and later operator overlays can reuse the same
  taxonomy;
- future retrieval debugging can trace artifacts back to the raw folder tree.

Do not flatten new categories into a single raw directory.

## 3. Preflight Checklist for a New Category

Before running ingestion, confirm:

- the category name and raw folder path are final enough to keep stable;
- filenames are understandable and do not need destructive bulk renaming;
- the category is within the supported insurance-document scope;
- you have 2 to 5 real user questions that the category should answer;
- you know whether the category needs curated `product` or `document_type`
  overlays;
- you know whether there are obvious aliases or synonyms that should be added
  to `ops/term-equivalences.json`.

Typical examples:

- `preguntas frecuentes`, `FAQ`, `faq`
- `propuesta de valor`, `pv`
- product aliases such as `bici`, `bicicleta`, `patineta`

## 4. Operator Artifacts You May Need

Not every new category needs all of these, but these are the main operator
controls.

### 4.1 Raw PDFs

- location: `data/raw/...`
- responsibility: source corpus and business taxonomy

### 4.2 Metadata overlays

- location: `ops/document-metadata-overlays.json`
- use when:
  - filename-derived metadata is ambiguous;
  - `document_type` must be curated explicitly;
  - `product` should be pinned to a canonical value.

Use overlays when canonical metadata matters for retrieval filters or citation
readability.

### 4.3 Term equivalences

- location: `ops/term-equivalences.json`
- use when:
  - real user vocabulary differs from document vocabulary;
  - stable aliases should normalize into canonical retrieval terms;
  - a repeated retrieval miss justifies a narrow deterministic expansion rule.

Do not use this file as a substitute for missing corpus evidence.

## 5. Standard Batch Workflow

The recommended local workflow is:

1. warm up Docling assets;
2. ingest the category;
3. inspect cleaned Markdown and chunks;
4. generate embeddings;
5. index into Qdrant;
6. validate retrieval;
7. validate a real grounded answer.

## 6. Commands

Use the external batch runtime, not the repo `.venv`, for heavy local
ingestion and embedding work.

### 6.1 Warm up Docling

```bash
make batch-warmup \
  BATCH_VENV=/private/tmp/yini-fast-venv311 \
  BATCH_SAMPLE_PDF="data/raw/MOVILIDAD/AUTOS/ayudaventas asistencia pequeños eventos.pdf"
```

### 6.2 Ingest only the target category

Example for `BICICLETAS Y PATINETAS`:

```bash
/private/tmp/yini-fast-venv311/bin/python -m rag.ingestion ingest-pdfs \
  --input-dir data/raw \
  --markdown-dir data/markdown \
  --processed-dir data/processed \
  --manifest-path data/processed/ingestion-manifest.jsonl \
  --glob "MOVILIDAD/BICICLETAS Y PATINETAS/*.pdf" \
  --metadata-overlay-path ops/document-metadata-overlays.json \
  --overwrite false \
  --fail-fast true \
  --pdf-conversion-backend docling \
  --docling-startup-timeout-seconds 1800
```

If you want to rerun the full incremental raw tree instead of a single
category, use `Makefile`:

```bash
make batch-ingest \
  BATCH_VENV=/private/tmp/yini-fast-venv311 \
  BATCH_INPUT_DIR=data/raw \
  BATCH_MARKDOWN_DIR=data/markdown \
  BATCH_PROCESSED_DIR=data/processed \
  BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json \
  BATCH_OVERWRITE=false
```

Important rule:

- use `--overwrite false` for normal incremental onboarding;
- use `--overwrite true` only when reprocessing an existing category after a
  code or metadata change.

### 6.2.1 Example: ingest only the `choque simple` transversal cohort

```bash
make batch-ingest \
  BATCH_VENV=/private/tmp/yini-fast-venv311 \
  BATCH_INPUT_DIR=data/raw \
  BATCH_MARKDOWN_DIR=data/markdown \
  BATCH_PROCESSED_DIR=data/processed \
  BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json \
  BATCH_GLOB='MOVILIDAD/TRANSVERSALES/*choque simple*.pdf' \
  BATCH_OVERWRITE=false
```

### 6.3 Generate embeddings only for the category

```bash
/private/tmp/yini-fast-venv311/bin/python -m rag.ingestion generate-embeddings \
  --chunk-dir data/processed/chunks \
  --embedding-dir data/processed/embeddings \
  --manifest-path data/processed/embedding-generation-manifest.jsonl \
  --glob "movilidad__bicicletas-y-patinetas__*.chunks.json" \
  --overwrite false \
  --fail-fast true
```

Example for the `choque simple` transversal cohort:

```bash
make batch-embeddings \
  BATCH_VENV=/private/tmp/yini-fast-venv311 \
  BATCH_PROCESSED_DIR=data/processed \
  BATCH_CHUNK_GLOB='movilidad__transversales__*choque-simple*.chunks.json' \
  BATCH_OVERWRITE=false
```

### 6.4 Index only the category into Qdrant

```bash
/private/tmp/yini-fast-venv311/bin/python -m rag.ingestion index-embeddings \
  --embedding-dir data/processed/embeddings \
  --manifest-path data/processed/qdrant-indexing-manifest.jsonl \
  --glob "movilidad__bicicletas-y-patinetas__*.embeddings.json" \
  --fail-fast true
```

Example for the `choque simple` transversal cohort:

```bash
make batch-index \
  BATCH_VENV=/private/tmp/yini-fast-venv311 \
  BATCH_PROCESSED_DIR=data/processed \
  BATCH_EMBEDDING_GLOB='movilidad__transversales__*choque-simple*.embeddings.json'
```

## 7. Inspection Gates

Do not jump directly from ingestion to production validation.

### Gate A — Markdown quality

Inspect:

- `data/markdown/*.md`
- `data/processed/*.cleaned.md`

Look for:

- broken headings;
- tables exploded into unusable text;
- repetitive page headers;
- image/embed noise promoted as titles;
- semantic sections collapsed into flat text.

### Gate B — Chunk quality

Inspect:

- `data/processed/chunks/*.chunks.json`

Look for:

- chunks that start with page markers instead of business content;
- chunks that mix unrelated sections;
- deductible, requirements, or comparison content split without context;
- short orphan chunks that should have inherited section context;
- missing category/product/document labels in payload metadata.

### Gate C — Retrieval quality

Run real category queries with `retrieve-chunks`.

Examples:

```bash
./.venv/bin/python -m rag.ingestion retrieve-chunks \
  --query "¿Qué cubre el seguro para bicicletas y patinetas?" \
  --top-k 8
```

```bash
./.venv/bin/python -m rag.ingestion retrieve-chunks \
  --query "¿Cuál es el deducible del seguro de bicicletas y patinetas?" \
  --top-k 12
```

Success condition:

- the target category appears in the top candidates with the expected document.

### Gate D — Grounded answer quality

Run at least one real query through answer generation.

Example:

```bash
./.venv/bin/python -m rag.ingestion answer-query \
  --query "¿Cuál es el deducible del seguro de bicicletas y patinetas?" \
  --top-k 8
```

Success condition:

- the answer is grounded;
- the citations reference the intended category evidence;
- the answer does not get crowded out by unrelated FAQs or weaker lexical hits.

## 8. What We Learned from AUTOS

`AUTOS` exposed these recurring patterns:

1. category retrieval may fail even when the corpus is already ingested;
2. comparative documents can exist in Qdrant but still lose ranking to FAQ
   text with stronger superficial overlap;
3. diagrammatic comparison tables may require ingestion-time normalization;
4. short follow-on fragments need inherited section context to remain useful;
5. category onboarding often needs query-alias tuning and narrow reranking
   before grounded answers become reliable.

Implication:

- a new category should always be validated with real retrieval queries, not
  just artifact existence.

## 9. What We Learned from BICICLETAS Y PATINETAS

`BICICLETAS Y PATINETAS` exposed these recurring patterns:

1. supported-scope admission can lag behind retrieval reality;
2. product aliases matter immediately in Spanish user vocabulary;
3. `pv` documents may be semantically valuable but diagrammatically noisy;
4. deductible and requirements sections often need stronger section-preserving
   normalization;
5. a correct document can be present in retrieval but still need evidence bias
   or recall tuning for specific intents such as `deducible`.

Implication:

- category onboarding is not complete until category-specific intent queries
  also succeed, not just generic coverage queries.

## 10. Symptom-to-Action Map

| Symptom | Likely cause | First action |
| --- | --- | --- |
| Query is refused as unsupported | Scope vocabulary is too narrow | Review `core/query_scope.py` and add a narrow corrective spec |
| Query retrieves wrong category | Missing aliases or product metadata drift | Review `ops/term-equivalences.json` and metadata overlays |
| Correct document exists but ranks low | Lexical or semantic crowd-out | Add a narrow retrieval corrective spec and inspect reranking |
| Chunk text is unreadable | Diagrammatic PDF extraction is weak | Normalize the specific section shape in ingestion |
| Document metadata is wrong | Filename/path inference is insufficient | Add or correct overlay entries |
| FAQ dominates business answer | Candidate pool or reranking is weak | Validate category-specific recall before changing prompts |

## 11. When to Open a Corrective Spec

Open a new dated spec bundle when:

- a category query fails after a successful ingestion run;
- a repeated alias mismatch appears in real queries;
- a specific document family has a recurring chunking defect;
- retrieval finds the right category but ranks the wrong evidence first;
- answer generation cites the wrong evidence even though retrieval contains the
  right document.

Open that bundle only when the root-cause family is meaningfully different from
the current active slice. Use these families:

- `taxonomy/scope`
- `ingestion/extraction`
- `index/runtime`
- `retrieval/ranking/answering`

Do not open a new dated bundle only because another query variant appears
inside the same root-cause family. Record those variants first in
`validation.md`.

Do not fold unrelated fixes into one category spec.

Preferred pattern:

1. identify one root-cause-sized failure family;
2. open one dated spec bundle for that family;
3. capture multiple representative query variants in `validation.md`;
4. validate with one or more real queries tied to that family;
5. close the slice before opening another bundle in the same category unless
   the seam changes.

Operational cap:

- keep at most `1` active onboarding bundle and `1` active remediation bundle
  per category at the same time;
- prefer at most `3` total bundles per category lifecycle:
  1. `baseline onboarding`
  2. `artifact/extraction remediation` when needed
  3. `retrieval/answer hardening`

## 12. Definition of Ready for a New Category

Before announcing a category as ready for broader usage, confirm:

- raw folder structure is stable;
- ingestion succeeded for the category files;
- cleaned Markdown and chunks were manually sampled;
- embeddings were generated;
- Qdrant indexing succeeded;
- at least one coverage query succeeded;
- at least one intent-specific query succeeded;
- metadata and aliases are aligned with actual retrieval-facing values;
- any known limitations are captured in specs or docs.

## 13. Recommended Rollout Pattern for Future Categories

Use this order:

1. ingest one category only;
2. validate one to three representative files first;
3. test two generic coverage questions;
4. test one intent-heavy question such as deductibles, requirements, or plan
   comparison;
5. patch the narrowest failure;
6. re-run only the affected artifacts;
7. promote the category after evidence is clean.

This avoids mixing multiple unknown category failures at once.

## 14. Practical Recommendation

For future onboarding, use this default sequence:

1. preserve the raw folder taxonomy;
2. ingest incrementally with `overwrite=false`;
3. inspect cleaned Markdown and chunks before embedding;
4. generate and index only the affected category;
5. validate retrieval before validating full answers;
6. use overlays for metadata truth, equivalence rules for vocabulary truth, and
   ingestion code changes only for structural extraction defects;
7. document each root-cause-sized corrective slice separately.

Default documentation shape for a new category:

1. one `baseline onboarding` bundle;
2. optionally one `artifact/extraction remediation` bundle if the extracted
   artifacts are not usable;
3. optionally one `retrieval/answer hardening` bundle that captures multiple
   query variants in the same seam before splitting again.

That is the route this repository should follow for every new category.
