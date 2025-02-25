.PHONY: docs tests

# Dependencies
dependencies:
	poetry install

# Tests
unit-tests:
	poetry run py.test --cov=pycaprio --cov-branch --cov-fail-under=90 tests/unit_tests

integ-tests:
	poetry run py.test --cov=pycaprio --cov-branch --cov-fail-under=90 tests/integ_tests

tests: unit-tests integ-tests

coverage:
	poetry run py.test --cov=pycaprio --cov-branch --cov-fail-under=90 --cov-report=xml:coverage.xml tests

format:
	poetry run ruff format pycaprio --line-length=120
	poetry run ruff format tests --line-length=120


# Static analysis/linting
lint:
	poetry run ruff check pycaprio --line-length=120 --fix
	poetry run ruff check tests --line-length=120 --fix --ignore=E722

# Docs
docs:
	poetry run mkdocs serve

# Building and publishing
build: unit-tests lint
	poetry build

publish: build
	poetry publish

# CI

ci-publish:
	poetry publish --build --username "${PYPI_USERNAME}" --password "${PYPI_PASSWORD}" --no-interaction

ci-bump-version:
	poetry run bump2version patch
