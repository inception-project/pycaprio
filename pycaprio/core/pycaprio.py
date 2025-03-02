import os
from typing import Optional

from pycaprio.core.adapters.http_adapter import HttpInceptionAdapter
from pycaprio.core.exceptions import ConfigurationNotProvided
from pycaprio.core.interfaces.types import authentication_type
from pycaprio.core.adapters.local_adapter import LocalInceptionAdapter


class Pycaprio:
    """
    Pycaprio client that can work with both remote INCEpTION API and local export projects in ZIP format.
    """

    def __init__(
        self,
        mode: str = "remote",
        inception_host: Optional[str] = None,
        authentication: Optional[authentication_type] = None,
        local_projects_dir: Optional[str] = None,
    ):
        """
        Initializes Pycaprio in either remote or local mode.
        
        :param mode: "remote" to connect to INCEpTION API, "local" to work with exported ZIPs.
        :param inception_host: INCEpTION server URL (only needed in remote mode).
        :param authentication: Tuple (username, password) for authentication (only needed in remote mode).
        :param local_projects_dir: Path to local directory containing exported ZIP projects (only needed in local mode).
        """
        self.mode = mode.lower()
        
        if self.mode == "remote":
            # Ensure remote credentials are provided
            inception_host = inception_host or os.getenv("INCEPTION_HOST")
            authentication = authentication or (os.getenv("INCEPTION_USERNAME"), os.getenv("INCEPTION_PASSWORD"))
            if not inception_host:
                raise ConfigurationNotProvided(
                    "Host was not provided. You can set it via environment variable as 'INCEPTION_HOST'"
                )
            if not all(authentication):
                raise ConfigurationNotProvided(
                    "Authentication was not provided. "
                    "You can set it via environment variables as 'INCEPTION_USERNAME' and 'INCEPTION_PASSWORD'"
                )
            self.api = HttpInceptionAdapter(inception_host, authentication)

        elif self.mode == "local":
            if not local_projects_dir:
                raise ConfigurationNotProvided("You must provide 'local_projects_dir' for local mode.")
            self.api = LocalInceptionAdapter(local_projects_dir)

        else:
            raise ValueError("Invalid mode. Use 'remote' for API mode or 'local' for local ZIP-based mode.")
