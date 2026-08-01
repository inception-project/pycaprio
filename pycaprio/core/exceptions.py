from typing import Optional

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


class IllegalIdentifier(InceptionBadResponse):
    """
    A project/document identifier was rejected by INCEpTION because it is not a numeric id.

    The remote API currently resolves projects and documents by numeric id only; passing a project
    name or URL slug makes it fail while parsing the value, which surfaces as an opaque HTTP 500
    carrying a Java NumberFormatException. This exception replaces that with an actionable message.

    Subclasses InceptionBadResponse so that existing handlers catching the generic bad-response
    error keep working.

    See https://github.com/inception-project/inception/issues/3457 for supporting slugs upstream.
    """

    def __init__(
        self,
        bad_response: requests.Response,
        parameter_name: str,
        identifier: object,
        lookup_hint: Optional[str] = None,
    ):
        super().__init__(bad_response)
        self.parameter_name = parameter_name
        self.identifier = identifier
        lookup_advice = (
            f" Look up the id first (e.g. via '{lookup_hint}') and pass that instead." if lookup_hint else ""
        )
        self.args = (
            f"{parameter_name.capitalize()} '{identifier}' was rejected by INCEpTION: the remote API "
            f"accepts only numeric {parameter_name} ids, not names or URL slugs.{lookup_advice}",
        )
