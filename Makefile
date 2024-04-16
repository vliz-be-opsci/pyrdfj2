TEST_PATH = ./tests/
FLAKE8_EXCLUDE = venv,.venv,.eggs,.tox,.git,__pycache__,*.pyc
PROJECT = pyrdfj2
AUTHOR = "Flanders Marine Institute, VLIZ vzw"

.PHONY: build docs clean install docker-build
.DEFAULT_GOAL := help

help:  ## Shows this list of available targets and their effect.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:
	@find . -name '*.pyc' -exec rm --force {} +
	@find . -name '*.pyo' -exec rm --force {} +
	@find . -name '*~' -exec rm --force {} +
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -f *.sqlite
	@rm -rf .cache

startup:
	@pip install --upgrade pip
	@which poetry >/dev/null || pip install poetry

init: startup  ## initial prepare of the environment for local execution of the package
	@poetry install

init-dev: startup  ## initial prepare of the environment for further development in the package
	@poetry install --with 'tests' --with 'dev' --with 'docs'
	@poetry run pre-commit install
	@poetry run pre-commit install --hook-type commit-msg

init-docs: startup  
	@poetry install --with 'docs'

docs:
	@if ! [ -d "./docs" ]; then poetry run sphinx-quickstart -q --ext-autodoc --sep --project $(PROJECT) --author $(AUTHOR) docs; fi
	@poetry run sphinx-apidoc -f -o ./docs/source ./$(PROJECT)
	@poetry run sphinx-build -E -a -b html ./docs/source ./docs/build/html

test:  ## runs the standard test-suite for the memory-graph implementation
	@poetry run pytest ${TEST_PATH}

test-coverage:  ## runs the standard test-suite for the memory-graph implementation and produces a coverage report
	@poetry run pytest --cov=$(PROJECT) ${TEST_PATH} --cov-report term-missing

check:  ## performs linting on the python code
	@poetry run black --check --diff .
	@poetry run isort --check --diff .
	@poetry run flake8 . --exclude ${FLAKE8_EXCLUDE}

lint-fix:  ## fixes code according to the lint suggestions
	@poetry run black .
	@poetry run isort .

docker-build:  ## builds a docker-callable variant of this (including dependencies)
	@docker build . -t pyrdfj2

update:  ## updates dependencies
	@poetry update
	@poetry run pre-commit autoupdate

build: update check test docs  ## builds the package
	@poetry build

release: build  ## releases the package
	@poetry release
