dependencies:
	poetry install

unit-tests:
	poetry run py.test tests/unit_tests

coverage:
	poetry run py.test --cov=pycaprio --cov-branch --cov-fail-under=90 --cov-report=html tests

lint:
	poetry run flake8 pycaprio --max-line-length=120
	poetry run flake8 tests --max-line-length=120 --ignore=E722

build: unit-tests lint
	poetry build

publish: build
	poetry publish
