import requests


class RetryableException(Exception):
    def __init__(self, bad_response: requests.Response):
        super().__init__()
        self.bad_response = bad_response
