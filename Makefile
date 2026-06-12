VENV ?= .venv
PYTHON_BIN ?= python3.11
PYTHON ?= $(VENV)/bin/python
PIP ?= $(VENV)/bin/pip
RUFF ?= $(VENV)/bin/ruff
PYTEST ?= $(VENV)/bin/pytest
BATCH_VENV ?= /private/tmp/yini-batch-venv
BATCH_PYTHON ?= $(BATCH_VENV)/bin/python
BATCH_PIP ?= $(BATCH_VENV)/bin/pip
BATCH_INPUT_DIR ?= data/raw
BATCH_MARKDOWN_DIR ?= /tmp/yini-batch/markdown
BATCH_PROCESSED_DIR ?= /tmp/yini-batch/processed
BATCH_INGEST_MANIFEST ?= $(BATCH_PROCESSED_DIR)/ingestion-manifest.jsonl
BATCH_EMBEDDING_MANIFEST ?= $(BATCH_PROCESSED_DIR)/embedding-generation-manifest.jsonl
BATCH_INDEX_MANIFEST ?= $(BATCH_PROCESSED_DIR)/qdrant-indexing-manifest.jsonl
BATCH_SAMPLE_PDF ?= $(BATCH_INPUT_DIR)/MOVILIDAD/AUTOS/ayudaventas asistencia pequeños eventos.pdf
BATCH_PDF_BACKEND ?= docling
BATCH_DOCLING_TIMEOUT ?= 600

.PHONY: setup lint test app run batch-setup batch-warmup batch-ingest batch-embeddings batch-index

setup:
	$(PYTHON_BIN) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev]

lint:
	$(RUFF) check .

test:
	$(PYTEST)

app:
	$(PYTHON) -m app.ui

run: app

batch-setup:
	$(PYTHON_BIN) -m venv $(BATCH_VENV)
	$(BATCH_PIP) install --upgrade pip
	$(BATCH_PIP) install -e .[dev]

batch-warmup:
	$(BATCH_PYTHON) -m rag.ingestion warmup-docling-assets \
		--sample-pdf "$(BATCH_SAMPLE_PDF)" \
		--docling-startup-timeout-seconds $(BATCH_DOCLING_TIMEOUT)

batch-ingest:
	mkdir -p "$(BATCH_MARKDOWN_DIR)" "$(BATCH_PROCESSED_DIR)"
	$(BATCH_PYTHON) -m rag.ingestion ingest-pdfs \
		--input-dir "$(BATCH_INPUT_DIR)" \
		--markdown-dir "$(BATCH_MARKDOWN_DIR)" \
		--processed-dir "$(BATCH_PROCESSED_DIR)" \
		--manifest-path "$(BATCH_INGEST_MANIFEST)" \
		--overwrite true \
		--fail-fast true \
		--pdf-conversion-backend "$(BATCH_PDF_BACKEND)" \
		--docling-startup-timeout-seconds $(BATCH_DOCLING_TIMEOUT)

batch-embeddings:
	$(BATCH_PYTHON) -m rag.ingestion generate-embeddings \
		--chunk-dir "$(BATCH_PROCESSED_DIR)/chunks" \
		--manifest-path "$(BATCH_EMBEDDING_MANIFEST)" \
		--overwrite true \
		--fail-fast true

batch-index:
	$(BATCH_PYTHON) -m rag.ingestion index-embeddings \
		--embedding-dir "$(BATCH_PROCESSED_DIR)/embeddings" \
		--manifest-path "$(BATCH_INDEX_MANIFEST)" \
		--fail-fast true
