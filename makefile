default:
	@cat makefile

env:
	python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update: env
	. env/bin/activate; pip install -r requirements.txt

lint:
	. env/bin/activate; pylint lab2/clean_ids.py || true

test: lint
	. env/bin/activate; pytest -vv tests

test_enrich:
	@. env/bin/activate && cat mock_transcripts.jsonl | python -u lab5/enrich_transcripts.py | python lab5/validate_schema.py
