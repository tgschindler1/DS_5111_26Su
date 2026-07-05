ENV = env
PYTHON = $(ENV)/bin/python3
PIP = $(ENV)/bin/pip
PYLINT = $(ENV)/bin/pylint
PYTEST = $(ENV)/bin/pytest

default:
	@cat makefile

env:
	python3 -m venv $(ENV)
	$(PIP) install --upgrade pip

update: env
	$(PIP) install -r requirements.txt

lint:
	$(PYTHON) -m pylint bin/ lib/ tests/

test: lint
	$(PYTEST) -vv tests

test_enrich:
	cat data/mock_transcripts.jsonl | $(PYTHON) -u bin/enrich_transcripts.py | $(PYTHON) bin/validate_schema.py
