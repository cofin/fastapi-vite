.PHONY: dev check fix clean cmd-exists-% install-deps-debian install-deps-osx


ifeq '$(findstring ;,$(PATH))' ';'
    detected_os := Windows
else
    detected_os := $(shell uname 2>/dev/null || echo Unknown)
    detected_os := $(patsubst CYGWIN%,Cygwin,$(detected_os))
    detected_os := $(patsubst MSYS%,MSYS,$(detected_os))
    detected_os := $(patsubst MINGW%,MSYS,$(detected_os))
endif
define osx_brew_install
	HOMEBREW_NO_AUTO_UPDATE=1 brew `brew ls --versions "$(1)" | wc -l | xargs expr | sed 's/0/install/' | sed 's/1/upgrade/'` "$(1)"
endef

ifneq (,$(wildcard ./.env))
    include .env
    export
	ENV_FILE_PARAM = --env-file .env
endif

cmd-exists-%:
	@hash $(*) > /dev/null 2>&1 || \
		(echo "ERROR: '$(*)' must be installed and available on your PATH."; exit 1)


clean:
	if [ -d "build" ]; then rm -r "build/*";  fi;
	if [ -d "dist" ]; then rm -r "dist/*";  fi;
	if [ -d ".pytest_cache" ]; then rm -r .pytest_cache;  fi;
	if [ -f ".coverage" ]; then rm -r .coverage; fi;


upgrade:
	poetry update


install-deps-osx:
	$(call osx_brew_install,python3)
	$(call osx_brew_install,ngrok)
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

install-deps-ubuntu:
	sudo apt update && sudo apt install -y build-essential python3
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -


install-runtime:
	poetry config virtualenvs.in-project true
	poetry install --no-dev


install:
	poetry config virtualenvs.in-project true
	poetry install


check:
	poetry run black --check fastapi_vite
	poetry run isort --check fastapi_vite --skip .venv
	poetry run flake8 fastapi_vite --exclude=node_modules,migrations
	poetry run pre-commit run

fix:
	poetry run pycln fastapi_vite --all --exclude '/(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|\.svn|_build|buck-out|build|dist|\.venv|node_modules)/'
	poetry run isort fastapi_vite --skip .venv
	poetry run black fastapi_vite --exclude '/(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|\.svn|_build|buck-out|build|dist|\.venv|node_modules)/'
