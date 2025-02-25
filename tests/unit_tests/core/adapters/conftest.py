from unittest.mock import Mock

import pytest

from pycaprio.core.adapters.http_adapter import HttpInceptionAdapter


@pytest.fixture
def mock_http_response():
    m = Mock()
    m.json.return_value = {"body": []}
    return m


@pytest.fixture
def mock_http_client(mock_http_response):
    return type(
        "MockHttpClient",
        (),
        {
            "get": Mock(return_value=mock_http_response),
            "post": Mock(return_value=mock_http_response),
            "delete": Mock(return_value=mock_http_response),
        },
    )


@pytest.fixture
def mock_http_adapter(mock_http_client):
    adapter = HttpInceptionAdapter("test-host", (None, None))
    adapter.client = mock_http_client
    return adapter
