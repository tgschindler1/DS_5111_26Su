ENV = env
PYTHON = $(ENV)/bin/python3
PIP = $(ENV)/bin/pip
PYLINT = $(ENV)/bin/pylint
PYTEST = $(ENV)/bin/pytest
DOCKERHUB_USERNAME ?= jzt6rv
IMAGE_NAME = ds5111-pipeline
IMAGE_TAG = latest
IMAGE_FULL = $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(IMAGE_TAG)
DATA_FILE = data/youtube_ids.txt
ENV_FILE = .env


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

.PHONY: load
load:
	@echo "Initiating Cloud Data Warehouse Synchronizer Node..."
	cat data/enriched_transcripts.jsonl | python bin/load_snowflake.py

.PHONY: docker-build docker-images docker-build-verify \
        test-clean-ids test-pipeline

docker-build:
	docker build -t $(IMAGE_FULL) .

docker-images:
	docker images

docker-build-verify: docker-build
	docker images | grep $(DOCKERHUB_USERNAME)/$(IMAGE_NAME)

test_clean_ids:
	cat $(DATA_FILE) | docker run -i $(IMAGE_FULL)

test_pipeline:
	cat $(DATA_FILE) | docker run -i --env-file $(ENV_FILE) $(IMAGE_FULL) \
		bash -c "python bin/clean_ids.py | python bin/extract_transcripts.py | python bin/enrich_transcripts.py | python bin/load_snowflake.py; cat logs/pipeline_audit.log"

pipeline-run:
	cat $(DATA_FILE) | docker run -i --env-file .env $(IMAGE_FULL)
