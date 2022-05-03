.DEFAULT_GOAL:=help
.ONESHELL:
PKGNAME=src/fastapi_vite
ENV_PREFIX=$(shell python3 -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
USING_POETRY=$(shell grep "tool.poetry" pyproject.toml && echo "yes")
USING_DOCKER=$(shell grep "TIMELY_USE_DOCKER=true" .env && echo "yes")
USING_PNPM=$(shell python3 -c "if __import__('pathlib').Path('pnpm-lock.yaml').exists(): print('yes')")
USING_YARN=$(shell python3 -c "if __import__('pathlib').Path('yarn.lock').exists(): print('yes')")
USING_NPM=$(shell python3 -c "if __import__('pathlib').Path('package-lock.json').exists(): print('yes')")
PYTHON_PACKAGES=$(shell poetry export -f requirements.txt  --without-hashes |cut -d'=' -f1 |cut -d ' ' -f1)
BUNDLE_VERSION=$(shell poetry version -s)
GRPC_PYTHON_BUILD_SYSTEM_ZLIB=true
FRONTEND_SRC_DIR=src/frontend
FRONTEND_BUILD_DIR=$(FRONTEND_SRC_DIR)/dist
BACKEND_SRC_DIR=src
BACKEND_BUILD_DIR=dist

.EXPORT_ALL_VARIABLES:

ifndef VERBOSE
.SILENT:
endif


REPO_INFO ?= $(shell git config --get remote.origin.url)
COMMIT_SHA ?= git-$(shell git rev-parse --short HEAD)

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


.PHONY: upgrade-dependencies
upgrade-dependencies:          ## Upgrade all dependencies to the latest stable versions
	@if [ "$(USING_POETRY)" ]; then poetry update; fi
	@echo "Python Dependencies Updated"
	@if [ "$(USING_NPM)" ]; then npm update --latest; fi
	@if [ "$(USING_YARN)" ]; then yarn upgrade; fi
	@if [ "$(USING_PNPM)" ]; then pnpm upgrade; fi
	@echo "Node Dependencies Updated"

###############
# lint & test #
###############
format-source: ## Format source code
	@echo 'Formatting and cleaning source...'
	./scripts/format-source-code.sh

lint: ## check style with flake8
	env PYTHONPATH=src poetry run flake8 src

test: ## run tests quickly with the default Python
	env PYTHONPATH=src:. poetry run pytest --cov-config .coveragerc --cov=src -l --tb=short tests
	env PYTHONPATH=src:. poetry run coverage report -m

test-frontend: ## run frontend tests using Cypress
	env ELECTRON_RUN_AS_NODE=1 npm run cy-run-ct-firefox

test-all: ## run tests on every Python version with tox
	env PYTHONPATH=src poetry run tox

coverage: ## check code coverage quickly with the default Python
	env PYTHONPATH=src/ poetry run coverage run --source gluentlib_contrib -m pytest --cov-config .coveragerc --cov-report term --cov-report html --cov=src
	env PYTHONPATH=src/ poetry run coverage report -m

.PHONY: install
install:          ## Install the project in dev mode.
	@if ! poetry --version > /dev/null; then echo 'poetry is required, install from https://python-poetry.org/'; exit 1; fi
	@if [ "$(USING_POETRY)" ]; then poetry config virtualenvs.in-project true && poetry install; fi
	@if [ "$(USING_NPM)" ]; then npm install; fi
	@echo "Install complete.  ** If you want to recreate your entire virtualenv run 'make virtualenv'"


.PHONY: licenses
licenses: 			## Generate licenses
	@echo "Generating Licenses"
	@poetry run pip-licenses --with-urls --format=markdown --packages ${PYTHON_PACKAGES}

.PHONY: license-file
license-file: 		## Generate licenses
	@echo "Generating License file"
	@poetry run pip-licenses --packages ${PYTHON_PACKAGES} --format=plain-vertical --with-license-file > LICENSE.md

###########
# version #
###########
version-bump-major: ## bump major version
	poetry run bump2version major
version-bump-minor: ## bump minor version
	poetry run bump2version --allow-dirty  minor
version-bump-patch: ## bump patch version
	poetry run bump2version patch

