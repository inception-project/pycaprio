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
        super().__init__()
        self.bad_response = bad_response
