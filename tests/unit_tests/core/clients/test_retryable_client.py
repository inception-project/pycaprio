import io
from unittest.mock import Mock
from urllib.parse import urlparse

import pytest

from pycaprio.core.clients.retryable_client import RetryableInceptionClient
from pycaprio.core.clients.retryable_client import SSLAdapter
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


def test_client_verifies_ssl_by_default(mock_host: str, mock_authentication: authentication_type):
    client = RetryableInceptionClient(mock_host, mock_authentication)
    assert client.session.verify is True


def test_client_verify_false_disables_verification(mock_host: str, mock_authentication: authentication_type):
    client = RetryableInceptionClient(mock_host, mock_authentication, verify=False)
    assert client.session.verify is False


def test_client_verify_string_is_used_as_ca_bundle_path(mock_host: str, mock_authentication: authentication_type):
    # A string verify is a path to a CA bundle and must be passed through to requests as-is,
    # not silently treated as "disable verification".
    client = RetryableInceptionClient(mock_host, mock_authentication, verify="/path/to/ca.pem")
    assert client.session.verify == "/path/to/ca.pem"


def test_client_ca_bundle_mounts_ssl_adapter(mocker, mock_host, mock_authentication, tmp_path):
    ca_bundle = tmp_path / "ca.pem"
    ca_bundle.write_text("dummy")
    # Avoid parsing the dummy CA file; we only care that the adapter gets mounted.
    mocker.patch("pycaprio.core.clients.retryable_client.create_urllib3_context", return_value=Mock())
    client = RetryableInceptionClient(mock_host, mock_authentication, ca_bundle=str(ca_bundle))
    assert isinstance(client.session.get_adapter("https://example.com"), SSLAdapter)


def test_client_ca_bundle_not_mounted_when_verification_disabled(mock_host, mock_authentication, tmp_path):
    ca_bundle = tmp_path / "ca.pem"
    ca_bundle.write_text("dummy")
    client = RetryableInceptionClient(mock_host, mock_authentication, ca_bundle=str(ca_bundle), verify=False)
    assert not isinstance(client.session.get_adapter("https://example.com"), SSLAdapter)


def test_client_missing_ca_bundle_raises(mock_host, mock_authentication, tmp_path):
    missing = tmp_path / "does-not-exist.pem"
    with pytest.raises(ValueError):
        RetryableInceptionClient(mock_host, mock_authentication, ca_bundle=str(missing))


def test_request_forwards_params_alongside_multipart_body(mocker, client: RetryableInceptionClient):
    # 'params' is the query string and is orthogonal to a multipart body, so it must still be
    # forwarded when form_data/files trigger the multipart-encoding branch of _request.
    session_request = mocker.patch.object(client.session, "request", return_value=Mock(status_code=200))
    client.post("test-url", files={"content": ("data", io.BytesIO(b"data"))}, params={"format": "text"})
    assert session_request.call_args.kwargs["params"] == {"format": "text"}
