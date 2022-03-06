import random
import io
import os

import pytest
import requests

from pycaprio import Pycaprio

TEST_INCEPTION_ENDPOINT = os.getenv("TEST_INCEPTION_ENDPOINT", default="http://localhost:8080")
TEST_USERNAME = os.getenv("TEST_USERNAME", default='test-remote')
TEST_PASSWORD = os.getenv("TEST_PASSWORD", default='test-remote')
TEST_PROJECT_PREFIX = os.getenv("TEST_PROJECT_PREFIX", default='testpycap')
TEST_CONTENT = "this is a whatever whatever test string"


def gen_test_name():
    return f"{TEST_PROJECT_PREFIX}{random.randint(0, 1000000000)}"


def is_inception_alive():
    return requests.get(TEST_INCEPTION_ENDPOINT).status_code == 200


def is_api_accessible():
    return requests.get(f"{TEST_INCEPTION_ENDPOINT}/swagger-ui/index.html").status_code == 200


@pytest.fixture(scope='session', autouse=True)
def pycaprio():
    if not is_inception_alive():
        raise Exception(f"Could not reach out INCEpTION on endpoint '{TEST_INCEPTION_ENDPOINT}")

    if not is_api_accessible():
        raise Exception("Cannot reach API endpoint, did you enable it?")

    client = Pycaprio(TEST_INCEPTION_ENDPOINT, authentication=(TEST_USERNAME, TEST_PASSWORD))
    yield client
    [client.api.delete_project(p) for p in client.api.projects() if p.project_name.startswith(TEST_PROJECT_PREFIX)]


@pytest.fixture
def test_name():
    return gen_test_name()


@pytest.fixture(scope='session', autouse=True)
def test_project(pycaprio):
    return pycaprio.api.create_project(gen_test_name())


@pytest.fixture
def test_io():
    return io.StringIO(TEST_CONTENT)


@pytest.fixture
def test_document(pycaprio, test_project):
    return pycaprio.api.create_document(test_project, gen_test_name(), io.StringIO(TEST_CONTENT))
