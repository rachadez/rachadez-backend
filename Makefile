PACKAGE_PATH = ./src
APP = $(PACKAGE_PATH)/__main__.py:create_app


.PHONY: install
run:
	poetry install

.PHONY: run
run:
	flask --app $(APP) run --reload