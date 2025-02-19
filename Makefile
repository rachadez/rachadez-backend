PACKAGE_PATH = ./src
APP = $(PACKAGE_PATH)/__main__.py:create_app
PYTHON3_BIN = $(shell which python3)

help:
	@echo "Available targets:"
	@echo "    install    - Install dependecies"
	@echo "    run        - Run the application"
	@echo "    db-up      - Create database container"
	@echo "    db-down    - Destroy database container"
	@echo "    help       - Display help message"

.PHONY: install
install:
	poetry install

.PHONY: run
run:
	flask --app $(APP) run --reload

.PHONY: run-dev
run-dev:
	$(PYTHON3_BIN) src/

.PHONY: db-up
db-up:
	docker compose up -d

.PHONY: db-down
db-down:
	docker compose down

.PHONY: build
build:
	docker build -t rachadez-backend .
