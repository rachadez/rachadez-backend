PACKAGE_PATH = ./src
APP = app/main.py
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
	poetry run fastapi run $(APP)

.PHONY: run-dev
run-dev:
	poetry run fastapi dev $(APP)
  
.PHONY: db-up
db-up:
	docker compose up -d

.PHONY: db-down
db-down:
	docker compose down

.PHONY: build
build:
	docker build -t rachadez-backend .
