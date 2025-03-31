import os
from typing import Optional

from pycaprio.core.adapters.http_adapter import HttpInceptionAdapter
from pycaprio.core.exceptions import ConfigurationNotProvided
from pycaprio.core.interfaces.types import authentication_type
from pycaprio.core.adapters.local_adapter import LocalInceptionAdapter


class Pycaprio:
    """
    Pycaprio client that can be initialized in either remote or local mode.
    """

    def __init__(
        self,
        inception_host: Optional[str] = None,
        authentication: Optional[authentication_type] = None,
        local_projects_dir: Optional[str] = None,
    ):
        """
        Initializes Pycaprio in either remote or local mode.

        :param inception_host: Hostname of the INCEpTION instance.
        :param authentication: Tuple of username and password for INCEpTION instance.
        :param local_projects_dir: Directory containing exported INCEpTION projects in ZIP format.
        """
        inception_host = inception_host or os.getenv("INCEPTION_HOST")
        if inception_host:
            authentication = authentication or (os.getenv("INCEPTION_USERNAME"), os.getenv("INCEPTION_PASSWORD"))
            if not all(authentication):
                raise ConfigurationNotProvided(
                    "Authentication was not provided. "
                    "You can set it via environment variables as 'INCEPTION_USERNAME' and 'INCEPTION_PASSWORD'"
                )
            
            self.api = HttpInceptionAdapter(inception_host, authentication)
        elif local_projects_dir:
            self.api = LocalInceptionAdapter(local_projects_dir)
        else:
            raise ConfigurationNotProvided(
                "Either inception_host and authentication or local_projects_dir must be provided."
            )