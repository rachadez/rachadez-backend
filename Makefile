PACKAGE_PATH = ./src
APP = app/main.py
PYTHON3_BIN = $(shell which python3)


.PHONY: install
install:
	poetry install

.PHONY: run
run:
	fastapi run $(APP)

.PHONY: run-dev
run-dev:
	fastapi dev $(APP)
