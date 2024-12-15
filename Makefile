PACKAGE_PATH = ./src
APP = $(PACKAGE_PATH)/__main__.py:create_app
PYTHON3_BIN = $(shell which python3)


.PHONY: install
install:
	poetry install

.PHONY: run
run:
	flask --app $(APP) run --reload

.PHONY: run-dev
run-dev:
	$(PYTHON3_BIN) src/