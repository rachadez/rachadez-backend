PACKAGE_PATH = ./src
APP = app/main.py
PYTHON3_BIN = $(shell which python3)


.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry ryn fastapi run $(APP)

.PHONY: run-dev
run-dev:
	poetry run fastapi dev $(APP)
