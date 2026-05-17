VENV ?= .venv
PYTHON_BIN ?= python3.11
PYTHON ?= $(VENV)/bin/python
PIP ?= $(VENV)/bin/pip
RUFF ?= $(VENV)/bin/ruff
PYTEST ?= $(VENV)/bin/pytest

.PHONY: setup lint test app run

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
