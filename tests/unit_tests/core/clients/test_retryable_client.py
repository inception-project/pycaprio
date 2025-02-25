from unittest.mock import Mock
from urllib.parse import urlparse

import pytest

from pycaprio.core.clients.retryable_client import RetryableInceptionClient
from pycaprio.core.exceptions import InceptionBadResponse
from pycaprio.core.interfaces.types import authentication_type


@pytest.mark.parametrize(
    "host, test_relative_url",
    [
        ("http://host/", "/test-relative"),
        ("http://host/", "test-relative"),
        ("http://host", "/test-relative"),
        ("http://host", "test-relative"),
    ],
)
def test_client_builds_full_url(host: str, test_relative_url: str, mock_authentication: authentication_type):
    client = RetryableInceptionClient(host, mock_authentication)
    assert bool(urlparse(client.build_url(test_relative_url)).netloc)


@pytest.mark.parametrize(
    "host, test_relative_url",
    [
        ("http://host", "test-relative"),
        ("http://host/", "test-relative"),
        ("http://host/", "/test-relative"),
        ("http://host", "/test-relative"),
    ],
)
def test_client_builds_correct_url(host: str, test_relative_url: str, mock_authentication: authentication_type):
    client = RetryableInceptionClient(host, mock_authentication)
    assert "http://host{api_path}/test-relative".format(api_path=client.INCEPTION_API_PATH) == client.build_url(
        test_relative_url
    )


def test_client_build_url_returns_url_as_is_if_absolute(client):
    absolute_url = "http://hello-this-is-a-test.com/api"
    assert absolute_url == client.build_url(absolute_url)


@pytest.mark.parametrize("http_verb", ["get", "post", "delete"])
def test_client_get_post_delete_calls_request_function(
    mock_request_function: Mock, client: RetryableInceptionClient, http_verb: str
):
    test_url = "test-url"
    getattr(RetryableInceptionClient, http_verb)(client, test_url)
    assert mock_request_function.called


@pytest.mark.parametrize("http_verb", ["get", "post", "delete"])
def test_client_get_post_delete_calls_request_function_with_correct_http_verb(
    mock_request_function: Mock, client: RetryableInceptionClient, http_verb: str
):
    test_url = "test-url"
    getattr(RetryableInceptionClient, http_verb)(client, test_url)
    assert mock_request_function.call_args[0][0] == http_verb


@pytest.mark.parametrize("http_verb", ["get", "post", "delete"])
def test_client_get_post_delete_calls_request_function_with_same_url(
    mock_request_function: Mock, client: RetryableInceptionClient, http_verb: str
):
    test_url = "test-url"
    getattr(RetryableInceptionClient, http_verb)(client, test_url)
    assert mock_request_function.call_args[0][1] == test_url


@pytest.mark.parametrize("http_verb", ["get", "post", "delete"])
def test_client_request_returns_inception_bad_request_if_already_retried(
    mocker, client: RetryableInceptionClient, http_verb
):
    retry_error = InceptionBadResponse(Mock())
    mocker.patch("pycaprio.core.clients.retryable_client.RetryableInceptionClient._request", side_effect=retry_error)
    mocker.patch("time.sleep")
    with pytest.raises(InceptionBadResponse):
        client.request(http_verb, "")
