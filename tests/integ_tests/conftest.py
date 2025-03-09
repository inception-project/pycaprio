import random
import io
import os
import time
import pytest
import requests
import bcrypt
import shlex
from testcontainers.core.container import DockerContainer
from pycaprio import Pycaprio
import docker

TEST_USERNAME = os.getenv("TEST_USERNAME", default="test-remote")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", default="test-remote")
TEST_PROJECT_PREFIX = os.getenv("TEST_PROJECT_PREFIX", default="testpycap")
TEST_CONTENT = "this is a whatever whatever test string"

def gen_test_name():
    return f"{TEST_PROJECT_PREFIX}{random.randint(0, 1000000000)}"

def is_inception_alive(endpoint):
    try:
        response = requests.get(f"{endpoint}/actuator/health")
        return response.status_code == 200 and response.json().get("status") == "UP"
    except requests.exceptions.RequestException:
        return False

def is_api_accessible(endpoint):
    try:
        return requests.get(f"{endpoint}/swagger-ui/index.html").status_code == 200
    except requests.exceptions.RequestException:
        return False

def is_docker_daemon_running():
    try:
        client = docker.from_env()
        client.ping()
        return True
    except docker.errors.DockerException:
        return False

@pytest.fixture(scope="session", autouse=True)
def inception_container():
    if not is_docker_daemon_running():
        pytest.skip("Docker daemon is not running. Skipping integration tests.")
    
    # Generate bcrypt hash from TEST_PASSWORD
    bcrypt_hash = bcrypt.hashpw(TEST_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    bcrypt_hash = f"{{bcrypt}}{bcrypt_hash}"
    escaped_bcrypt_hash = bcrypt_hash.replace("$", "\\$")

    print("Starting INCEpTION container...")
    print(f"Using username '{TEST_USERNAME}' and password '{TEST_PASSWORD}'")

    container = DockerContainer("ghcr.io/inception-project/inception:latest")
    container.with_env(
        "JAVA_OPTS",
        " ".join([
            "-Dremote-api.enabled=true",
            f"-Dsecurity.default-admin-username={TEST_USERNAME}",
            f"-Dsecurity.default-admin-password={escaped_bcrypt_hash}",
            "-Dsecurity.default-admin-remote-access=true"
        ])
    )
    container.with_exposed_ports(8080)
    container.start()

    # Custom health check
    max_retries = 300
    inception_endpoint = f"http://localhost:{container.get_exposed_port(8080)}"
    for _ in range(max_retries):
        if is_inception_alive(inception_endpoint):
            break
        time.sleep(1)
    else:
        container.stop()
        pytest.fail("INCEpTION container did not become healthy in time.")

    yield container, inception_endpoint
    container.stop()

@pytest.fixture(scope="session", autouse=True)
def pycaprio(inception_container):
    container, inception_endpoint = inception_container
    if not is_inception_alive(inception_endpoint):
        raise Exception(f"Could not reach INCEpTION on endpoint '{inception_endpoint}'")

    if not is_api_accessible(inception_endpoint):
        raise Exception("Cannot reach API endpoint, did you enable it?")

    client = Pycaprio(inception_endpoint, authentication=(TEST_USERNAME, TEST_PASSWORD))
    yield client
    [client.api.delete_project(p) for p in client.api.projects() if p.project_name.startswith(TEST_PROJECT_PREFIX)]

@pytest.fixture
def test_name():
    return gen_test_name()

@pytest.fixture(scope="session", autouse=True)
def test_project(pycaprio):
    return pycaprio.api.create_project(gen_test_name())

@pytest.fixture
def test_io():
    return io.StringIO(TEST_CONTENT)

@pytest.fixture
def test_document(pycaprio, test_project):
    return pycaprio.api.create_document(test_project, gen_test_name(), io.StringIO(TEST_CONTENT))
