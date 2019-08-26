import os
from typing import Optional

from pycaprio.core.adapters.http_adapter import HttpInceptionAdapter
from pycaprio.core.exceptions import ConfigurationNotProvided
from pycaprio.core.interfaces.types import authentication_type


class Pycaprio:
    api = HttpInceptionAdapter

    def __init__(self, inception_host: Optional[str] = None, authentication: Optional[authentication_type] = None):
        inception_host = inception_host or os.getenv('INCEPTION_HOST')
        authentication = authentication or (os.getenv('INCEPTION_USERNAME'), os.getenv('INCEPTION_PASSWORD'))
        if not inception_host:
            raise ConfigurationNotProvided(
                "Host was not provided. You can set it via environment variable as 'INCEPTION_HOST'")
        if not all(authentication):
            raise ConfigurationNotProvided(
                "Authentication was not provided. "
                "You can set it via environment variables as 'INCEPTION_USERNAME' and 'INCEPTION_PASSWORD'")

        self.api = HttpInceptionAdapter(inception_host, authentication)
