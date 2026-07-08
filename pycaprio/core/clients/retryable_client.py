import io
import os
import time
from typing import Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from requests_toolbelt import MultipartEncoder

from pycaprio.core.exceptions import InceptionBadResponse
from pycaprio.core.interfaces.client import BaseInceptionClient
from pycaprio.core.interfaces.types import authentication_type


class SSLAdapter(HTTPAdapter):
    """
    Custom HTTPAdapter that allows merging custom CA certificates with the system default certificates.
    This enables trusting both system CAs and custom/self-signed certificates.
    """

    def __init__(self, ca_bundle: Optional[str] = None, **kwargs):
        self.ca_bundle = ca_bundle
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        """Initialize pool manager with custom SSL context that includes custom CA certificates."""
        if self.ca_bundle:
            ctx = create_urllib3_context()
            # Load the system default CAs first, then add the custom CA bundle on top so that
            # both system-trusted and custom/self-signed certificates are trusted.
            ctx.load_default_certs()
            ctx.load_verify_locations(cafile=self.ca_bundle)
            kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)


class RetryableInceptionClient(BaseInceptionClient):
    """
    HTTP client which implements retrying with exponential backoff.
    Documentation is described in 'BaseInceptionClient'.
    """

    RETRY_STATUSES = (408, 502, 503, 504)

    def __init__(
        self,
        inception_host: str,
        authentication: authentication_type,
        max_retries: int = 3,
        ca_bundle: Optional[str] = None,
        verify: Union[bool, str] = True,
    ):
        super().__init__(inception_host, authentication)
        self.session = requests.Session()
        self.session.auth = authentication
        assert 0 < max_retries, "max_retries must be greater than 0"
        self.max_retries = max_retries

        if ca_bundle is not None and not os.path.isfile(ca_bundle):
            raise ValueError(f"CA bundle file does not exist or is not a file: {ca_bundle}")

        # requests natively accepts verify as a bool or a path to a CA bundle.
        self.session.verify = verify

        # Mount custom SSL adapter if we have a custom CA bundle and verification is not disabled.
        # This trusts the custom CA in addition to the system CAs.
        if ca_bundle and verify is not False:
            self.session.mount("https://", SSLAdapter(ca_bundle=ca_bundle))

    def get(self, url: str, params: Optional[dict] = None) -> requests.Response:
        return self.request("get", url, params=params)

    def post(
        self,
        url: str,
        data: Optional[dict] = None,
        form_data: Optional[dict] = None,
        files: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> requests.Response:
        return self.request("post", url, data=data, form_data=form_data, files=files, params=params)

    def delete(self, url: str, params: Optional[dict] = None) -> requests.Response:
        return self.request("delete", url, params=params)

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
        self,
        method: str,
        url: str,
        form_data: Optional[dict] = None,
        files: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs,
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
            # 'params' is the query string, orthogonal to the multipart body, so it must be forwarded
            # here too. ('data' is intentionally not forwarded: it would collide with the multipart body.)
            multipart_encoder = MultipartEncoder(fields={**form_data, **files})
            response = self.session.request(
                method,
                url,
                data=multipart_encoder,
                params=params,
                headers={"Content-Type": multipart_encoder.content_type},
            )
        else:
            response = self.session.request(method, url, params=params, **kwargs)
        if 200 <= response.status_code < 300:
            return response
        else:
            raise InceptionBadResponse(response)
