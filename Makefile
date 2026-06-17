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
BATCH_METADATA_OVERLAY_PATH ?= ops/document-metadata-overlays.json
BATCH_INGEST_MANIFEST ?= $(BATCH_PROCESSED_DIR)/ingestion-manifest.jsonl
BATCH_EMBEDDING_MANIFEST ?= $(BATCH_PROCESSED_DIR)/embedding-generation-manifest.jsonl
BATCH_INDEX_MANIFEST ?= $(BATCH_PROCESSED_DIR)/qdrant-indexing-manifest.jsonl
BATCH_SAMPLE_PDF ?= $(BATCH_INPUT_DIR)/MOVILIDAD/AUTOS/ayudaventas asistencia pequeños eventos.pdf
BATCH_PDF_BACKEND ?= docling
BATCH_DOCLING_TIMEOUT ?= 1800
BATCH_OVERWRITE ?= false
BATCH_GLOB ?= **/*.pdf
BATCH_CHUNK_GLOB ?= *.chunks.json
BATCH_EMBEDDING_GLOB ?= *.embeddings.json

.PHONY: setup lint test test-release app run batch-setup batch-warmup batch-ingest batch-embeddings batch-index

setup:
	$(PYTHON_BIN) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev]

lint:
	$(RUFF) check .

test:
	$(PYTEST)

test-release:
	PYTHONPATH=. $(PYTEST) tests/test_evaluation_dataset.py tests/test_evaluation_runner.py tests/test_smoke.py -q
	PYTHONPATH=. $(PYTEST) tests/test_mcp_server.py tests/test_mcp_client.py tests/test_mcp_compatibility.py tests/test_mcp_versioning.py -q
	PYTHONPATH=. $(PYTEST) tests/test_app_ui.py tests/test_observability.py tests/test_query_scope.py tests/test_guardrail_abuse_cases.py tests/test_langgraph_workflow.py -q
	PYTHONPATH=. $(PYTEST) tests/test_retrieval.py tests/test_grounded_answer_generation.py tests/test_document_canonicalization.py tests/test_term_equivalences.py tests/test_embedding_generation.py tests/test_qdrant_indexing.py tests/test_cli_runtime.py tests/test_ingestion.py -q

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
		--glob "$(BATCH_GLOB)" \
		--metadata-overlay-path "$(BATCH_METADATA_OVERLAY_PATH)" \
		--overwrite "$(BATCH_OVERWRITE)" \
		--fail-fast true \
		--pdf-conversion-backend "$(BATCH_PDF_BACKEND)" \
		--docling-startup-timeout-seconds $(BATCH_DOCLING_TIMEOUT)

batch-embeddings:
	$(BATCH_PYTHON) -m rag.ingestion generate-embeddings \
		--chunk-dir "$(BATCH_PROCESSED_DIR)/chunks" \
		--manifest-path "$(BATCH_EMBEDDING_MANIFEST)" \
		--glob "$(BATCH_CHUNK_GLOB)" \
		--overwrite "$(BATCH_OVERWRITE)" \
		--fail-fast true

batch-index:
	$(BATCH_PYTHON) -m rag.ingestion index-embeddings \
		--embedding-dir "$(BATCH_PROCESSED_DIR)/embeddings" \
		--manifest-path "$(BATCH_INDEX_MANIFEST)" \
		--glob "$(BATCH_EMBEDDING_GLOB)" \
		--fail-fast true
