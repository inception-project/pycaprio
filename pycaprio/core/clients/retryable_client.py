import io
import time
from typing import Optional

import requests
from requests_toolbelt import MultipartEncoder

from pycaprio.core.exceptions import InceptionBadResponse
from pycaprio.core.interfaces.client import BaseInceptionClient
from pycaprio.core.interfaces.types import authentication_type


class RetryableInceptionClient(BaseInceptionClient):
    """
    HTTP client which implements retrying with exponential backoff.
    Documentation is described in 'BaseInceptionClient'.
    """

    RETRY_STATUSES = (408, 502, 503, 504)

    def __init__(self, inception_host: str, authentication: authentication_type, max_retries=3):
        super().__init__(inception_host, authentication)
        self.session = requests.Session()
        self.session.auth = authentication
        assert 0 < max_retries, "max_retries must be greater than 0"
        self.max_retries = max_retries

    def get(self, url: str, params: Optional[dict] = None) -> requests.Response:
        return self.request("get", url, params=params)

    def post(
        self, url: str, data: Optional[dict] = None, form_data: Optional[dict] = None, files: Optional[dict] = None
    ) -> requests.Response:
        return self.request("post", url, data=data, form_data=form_data, files=files)

    def delete(self, url: str) -> requests.Response:
        return self.request("delete", url)

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        retries = 0
        retry = False
        last_error = None

        while (retry and retries < self.max_retries) or retries == 0:
            time.sleep((2**retries) / 10)
            try:
                return self._request(method, url, **kwargs)
            except InceptionBadResponse as bad_response_error:
                last_error = bad_response_error
                retry = method == "get" and bad_response_error.status_code in self.RETRY_STATUSES

            retries += 1
        raise last_error

    def _request(
        self, method: str, url: str, form_data: Optional[dict] = None, files: Optional[dict] = None, **kwargs
    ) -> requests.Response:
        form_data = form_data or {}
        files = files or {}
        url = self.build_url(url)
        if files:
            # Rewind file's IO streams
            if file_content := files.get("content"):
                _, io_stream = file_content
                io_stream.seek(0, io.SEEK_SET)

        if form_data or files:  # Correctly encode multiform data
            multipart_encoder = MultipartEncoder(fields={**form_data, **files})
            response = self.session.request(
                method, url, data=multipart_encoder, headers={"Content-Type": multipart_encoder.content_type}
            )
        else:
            response = self.session.request(method, url, **kwargs)
        if 200 <= response.status_code < 300:
            return response
        else:
            raise InceptionBadResponse(response)
