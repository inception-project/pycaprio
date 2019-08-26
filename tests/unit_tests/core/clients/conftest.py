from unittest.mock import Mock

import pytest
from pytest_mock import MockFixture

from pycaprio.core.clients.retryable_client import RetryableInceptionClient
from pycaprio.core.interfaces.types import authentication_type


@pytest.fixture
def mock_host() -> str:
    return "http://inception-test.com"


@pytest.fixture
def mock_authentication() -> authentication_type:
    return 'test', 'test'


@pytest.fixture
def client(mock_host: str, mock_authentication: authentication_type) -> RetryableInceptionClient:
    return RetryableInceptionClient(mock_host, mock_authentication)


@pytest.fixture
def mock_request_function(mocker: MockFixture) -> Mock:
    mocked_request = mocker.patch('pycaprio.core.clients.retryable_client.RetryableInceptionClient.request')
    return mocked_request
