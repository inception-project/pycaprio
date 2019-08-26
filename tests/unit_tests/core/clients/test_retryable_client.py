from unittest.mock import Mock
from urllib.parse import urlparse

import pytest
from tenacity import RetryError

from pycaprio.core.clients.exceptions import RetryableException
from pycaprio.core.clients.retryable_client import RetryableInceptionClient
from pycaprio.core.exceptions import InceptionBadResponse
from pycaprio.core.interfaces.types import authentication_type
from pycaprio.core.interfaces.types import status_list_type


@pytest.mark.parametrize("host, test_relative_url", [('http://host/', '/test-relative'),
                                                     ('http://host/', 'test-relative'),
                                                     ('http://host', '/test-relative'),
                                                     ('http://host', 'test-relative')])
def test_client_builds_full_url(host: str, test_relative_url: str, mock_authentication: authentication_type):
    client = RetryableInceptionClient(host, mock_authentication)
    assert bool(urlparse(client.build_url(test_relative_url)).netloc)


@pytest.mark.parametrize("host, test_relative_url", [('http://host', 'test-relative'),
                                                     ('http://host/', 'test-relative'),
                                                     ('http://host/', '/test-relative'),
                                                     ('http://host', '/test-relative'), ])
def test_client_builds_correct_url(host: str, test_relative_url: str, mock_authentication: authentication_type):
    client = RetryableInceptionClient(host, mock_authentication)
    assert "http://host{api_path}/test-relative".format(api_path=client.INCEPTION_API_PATH) == client.build_url(
        test_relative_url)


def test_client_build_url_returns_url_as_is_if_absolute(client):
    absolute_url = "http://hello-this-is-a-test.com/api"
    assert absolute_url == client.build_url(absolute_url)


@pytest.mark.parametrize("http_verb", ['get', 'post', 'delete'])
def test_client_get_post_delete_calls_request_function(mock_request_function: Mock,
                                                       client: RetryableInceptionClient,
                                                       http_verb: str):
    test_url = "test-url"
    getattr(RetryableInceptionClient, http_verb)(client, test_url)
    assert mock_request_function.called


@pytest.mark.parametrize("http_verb", ['get', 'post', 'delete'])
def test_client_get_post_delete_calls_request_function_with_correct_http_verb(mock_request_function: Mock,
                                                                              client: RetryableInceptionClient,
                                                                              http_verb: str):
    test_url = "test-url"
    getattr(RetryableInceptionClient, http_verb)(client, test_url)
    assert mock_request_function.call_args[0][0] == http_verb


@pytest.mark.parametrize("http_verb", ['get', 'post', 'delete'])
def test_client_get_post_delete_calls_request_function_with_same_url(mock_request_function: Mock,
                                                                     client: RetryableInceptionClient,
                                                                     http_verb: str):
    test_url = "test-url"
    getattr(RetryableInceptionClient, http_verb)(client, test_url)
    assert mock_request_function.call_args[0][1] == test_url


@pytest.mark.parametrize("http_verb", ['get', 'post', 'delete'])
def test_client_get_post_delete_calls_request_function_with_same_allowed_status(mock_request_function: Mock,
                                                                                client: RetryableInceptionClient,
                                                                                http_verb: str):
    test_url = "test-url"
    test_allowed_statuses = [1, 2, 3]
    getattr(RetryableInceptionClient, http_verb)(client, test_url, allowed_statuses=test_allowed_statuses)
    assert mock_request_function.call_args[0][2] == test_allowed_statuses


def test_client_post_form_data_translates_into_files_none(mock_request_function: Mock,
                                                          client: RetryableInceptionClient):
    test_url = "test-url"
    form_data = {'test': 'test-value'}
    client.post(test_url, form_data=form_data, files=None)
    assert mock_request_function.call_args[1]['files'] == {'test': (None, form_data['test'])}


def test_client_post_form_data_translates_into_files_empty_dict(mock_request_function: Mock,
                                                                client: RetryableInceptionClient):
    test_url = "test-url"
    form_data = {'test': 'test-value'}
    client.post(test_url, form_data=form_data, files={})
    assert mock_request_function.call_args[1]['files'] == {'test': (None, form_data['test'])}


def test_client_post_form_data_translates_into_files_not_overwrite(mock_request_function: Mock,
                                                                   client: RetryableInceptionClient):
    test_url = "test-url"
    form_data = {'test': 'test-value'}
    files = {'example': (None, None)}
    client.post(test_url, form_data=form_data, files=files)
    assert mock_request_function.call_args[1]['files'] == {'test': (None, form_data['test']),
                                                           'example': files['example']}


@pytest.mark.parametrize("http_verb", ['get', 'post', 'delete'])
def test_client_request_returns_inception_bad_request_if_already_retried(mocker, client: RetryableInceptionClient,
                                                                         http_verb):
    retry_error = RetryError(Mock())
    mocker.patch('pycaprio.core.clients.retryable_client.RetryableInceptionClient._request', side_effect=retry_error)
    with pytest.raises(InceptionBadResponse):
        client.request(http_verb, "", (1, 2, 3))


def do_mocked_request(mocker, client: RetryableInceptionClient, allowed_statuses: status_list_type,
                      response_status_code: int,
                      *args, **kwargs):
    mocker.patch('tenacity.BaseRetrying.wraps', return_value=lambda f: f)
    client.session = Mock()
    client.session.request = Mock(return_value=type('MockedResponse', (), {'status_code': response_status_code}))
    response = client._request.__wrapped__(client, "test-verb", "test-url", allowed_statuses=allowed_statuses, *args,
                                           **kwargs)
    return response


def test_status_code_in_no_retry_list_not_allowed_raise_exception(mocker, client: RetryableInceptionClient):
    response_status_code = 404
    client.NO_RETRY_STATUSES = [response_status_code]
    with pytest.raises(InceptionBadResponse):
        do_mocked_request(mocker, client, (response_status_code + 1,), response_status_code)


def test_status_code_in_no_retry_list_but_allowed_no_raise_exception(mocker, client: RetryableInceptionClient):
    response_status_code = 404
    client.NO_RETRY_STATUSES = [response_status_code]
    try:
        do_mocked_request(mocker, client, (response_status_code,), response_status_code)
    except RetryableException:
        pytest.fail()


def test_status_not_allowed_and_retryable_raise_exception(mocker, client: RetryableInceptionClient):
    response_status_code = 500
    client.NO_RETRY_STATUSES = [response_status_code + 1]
    with pytest.raises(RetryableException):
        do_mocked_request(mocker, client, (response_status_code + 2,), response_status_code)


def test_status_allowed_and_retryable_no_raise_exception(mocker, client: RetryableInceptionClient):
    response_status_code = 500
    client.NO_RETRY_STATUSES = [response_status_code + 1]
    try:
        do_mocked_request(mocker, client, (response_status_code,), response_status_code)
    except RetryableException:
        pytest.fail()
