from abc import ABCMeta
from abc import abstractmethod
from typing import Optional
from urllib.parse import urlparse

import requests

from pycaprio.core.interfaces.types import authentication_type


class BaseInceptionClient(metaclass=ABCMeta):
    INCEPTION_API_PATH = "/api/aero/v1"

    def __init__(self, inception_host: str, authentication: Optional[authentication_type] = None):
        """
        Interface for the InceptionClient.
        :param inception_host: Inception host. This would be an url pointing to your inception machine.
        :param authentication: username, password tuple. User must have a remote role.
        """
        self.inception_host = inception_host[:-1] if inception_host[-1] == "/" else inception_host
        self.authentication = authentication

    def build_url(self, relative_url: str) -> str:
        """
        Builds whole url like: inception_host + /api/aero/v1 + url
        :param relative_url:
        :return:
        """
        url_is_absolute = bool(urlparse(relative_url).netloc)
        if url_is_absolute:
            return relative_url
        relative_url = "/" + relative_url if relative_url[0] != "/" else relative_url
        return f"{self.inception_host}{self.INCEPTION_API_PATH}{relative_url}"

    @abstractmethod
    def get(self, url: str, data: Optional[dict]) -> requests.Response:
        """
        Issues an authenticated GET request to Inception
        :param url: relative url to make request
        :param data: Parameters to include in the request
        :return: Response
        """
        pass  # pragma: no cover

    @abstractmethod
    def post(self, url: str, json: dict, files: dict) -> requests.Response:
        """
        Issues an authenticated POST request to Inception
        :param url: relative url to make request
        :param json: JSON body
        :param files: Files to be uploaded.
        :return: Response
        """
        pass  # pragma: no cover

    @abstractmethod
    def delete(self, url: str) -> requests.Response:
        """
        Issues an authenticated DELETE request to Inception
        :param url: relative url to make request
        :return: Response
        """
        pass  # pragma: no cover

    @abstractmethod
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Issues an authenticated request to Inception
        :param url: relative url to make request
        :return: Response
        """
        pass  # pragma: no cover
