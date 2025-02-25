import requests


class ConfigurationNotProvided(Exception):
    """
    Bad/Missing configuration
    """

    pass


class InceptionBadResponse(Exception):
    """
    Unexpected response from INCEpTION
    """

    def __init__(self, bad_response: requests.Response):
        super().__init__(f"HTTP {bad_response.status_code}: {bad_response.text}")
        self.bad_response = bad_response
        self.status_code = bad_response.status_code
