from typing import Optional

import requests
from tenacity import RetryError
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt

from pycaprio.core.exceptions import InceptionBadResponse
from pycaprio.core.interfaces.client import BaseInceptionClient
from pycaprio.core.clients.exceptions import RetryableException
from pycaprio.core.interfaces.types import authentication_type
from pycaprio.core.interfaces.types import status_list_type


class RetryableInceptionClient(BaseInceptionClient):
    """
    HTTP client which implements retrying by default.
    Documentation is described in 'BaseInceptionClient'.
    """
    MAX_RETRY_ATTEMPTS = 5
    NO_RETRY_STATUSES = (404, 401, 403)

    def __init__(self, inception_host: str, authentication: authentication_type):
        super().__init__(inception_host, authentication)
        self.session = requests.Session()
        self.session.auth = authentication

    def get(self, url: str, params: Optional[dict] = None,
            allowed_statuses: Optional[status_list_type] = None) -> requests.Response:
        return self.request('get', url, allowed_statuses, params=params)

    def post(self, url: str, data: Optional[dict] = None, form_data: Optional[dict] = None, json: Optional[dict] = None,
             files: Optional[dict] = None,
             allowed_statuses: Optional[status_list_type] = None) -> requests.Response:
        if form_data:
            files = files or {}
            for k, v in form_data.items():
                files[k] = (None, v)
        return self.request('post', url, allowed_statuses, data=data, json=json, files=files)

    def delete(self, url: str, allowed_statuses: Optional[status_list_type] = None) -> requests.Response:
        return self.request('delete', url, allowed_statuses)

    def request(self, method: str, url: str, allowed_statuses: Optional[status_list_type],
                **kwargs) -> requests.Response:
        try:
            return self._request(method, url, allowed_statuses, **kwargs)
        except RetryError as retry_error:
            raise InceptionBadResponse(retry_error.last_attempt._exception.bad_response)

    @retry(retry=retry_if_exception_type(RetryableException), stop=stop_after_attempt(MAX_RETRY_ATTEMPTS))
    def _request(self, method: str, url: str, allowed_statuses: Optional[status_list_type],
                 **kwargs) -> requests.Response:

        url = self.build_url(url)

        allowed_statuses = allowed_statuses or tuple()
        response = self.session.request(method, url, **kwargs)

        # Retry if status code is retryable and not allowed
        status_code_is_retryable = response.status_code not in self.NO_RETRY_STATUSES
        status_code_is_not_allowed = allowed_statuses and (response.status_code not in allowed_statuses)

        if status_code_is_retryable and status_code_is_not_allowed:
            raise RetryableException(response)
        elif status_code_is_not_allowed:
            raise InceptionBadResponse(response)

        return response
