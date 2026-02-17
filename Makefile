PY=python3

install:
	$(PY) -m pip install -r requirements.txt

migrate:
	./migrations/001_init_version.sh

dev: migrate
	$(PY) src/main.py

test:
	pytest
