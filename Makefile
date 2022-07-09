.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

install: ## install dependencies
	pip install poetry==1.1.14
	poetry install --no-root

clean: clean-build clean-pyc clean-cache

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-cache: ## remove .cache and .pytest_cache
	rm -rf .cache
	rm -rf .pytest_cache

lint: ## check style with flake8
	poetry run flake8

test: ## run tests quickly with the default Python
	poetry run pytest

test-all: ## run tests on every Python version with tox
	poetry run tox --skip-missing-interpreters

coverage: ## check code coverage quickly with the default Python
	rm -rf htmlcov
	poetry run coverage erase
	poetry run coverage run -m pytest
	poetry run coverage report -m
	poetry run coverage html

docs: ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

release: sdist ## package and upload a release
	pipenv run twine upload dist/*

build: clean ## package
	poetry build
	# gpg --detach-sign -a dist/*.tar.gz
	ls -l dist
