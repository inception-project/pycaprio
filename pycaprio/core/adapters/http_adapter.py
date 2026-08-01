import os
import re
from typing import IO, Union, List, Optional
from urllib.parse import quote

from pycaprio.core.clients.retryable_client import RetryableInceptionClient
from pycaprio.core.exceptions import IllegalIdentifier
from pycaprio.core.exceptions import InceptionBadResponse
from pycaprio.core.interfaces.adapter import BaseInceptionAdapter
from pycaprio.core.interfaces.client import BaseInceptionClient
from pycaprio.core.interfaces.types import authentication_type
from pycaprio.core.mappings import AnnotationState
from pycaprio.core.mappings import InceptionFormat
from pycaprio.core.mappings import DocumentState
from pycaprio.core.objects.annotation import Annotation
from pycaprio.core.objects.document import Document
from pycaprio.core.objects.project import Project
from pycaprio.core.objects.curation import Curation
from pycaprio.core.schemas.annotation import AnnotationSchema
from pycaprio.core.schemas.document import DocumentSchema
from pycaprio.core.schemas.project import ProjectSchema
from pycaprio.core.schemas.curation import CurationSchema


def _resolve_document_filename(content: IO, filename: Optional[str] = None) -> str:
    """
    Determines the file name to send for a document upload. This only sets the name recorded for the
    uploaded file; the content format is determined by the format id sent alongside it, not by this
    name or its extension. An explicit ``filename`` wins; otherwise the base name of the passed file
    object is used (if it is a real, named file). Raises ``ValueError`` when neither is available,
    rather than silently uploading under a meaningless placeholder name.
    """
    if filename:
        return filename
    name = getattr(content, "name", None)
    if isinstance(name, (str, bytes)) and name:
        base = os.path.basename(name)  # accepts str or bytes; a bytes path yields a bytes basename
        if base:
            return os.fsdecode(base)
    raise ValueError(
        "Could not determine a file name for the document upload. Pass an explicit 'filename', or "
        "provide a 'content' file object with a 'name' attribute (e.g. one opened with open(...))."
    )


# Matches INCEpTION failing to convert a path variable into a numeric id, capturing the value it
# could not parse and, when the server reports it, the parameter it was binding. The exact wording
# varies across versions -- older releases report a nested 'java.lang.NumberFormatException' (see
# issue #15) and name no parameter, newer ones say "Method parameter 'projectId': Failed to convert
# value of type 'java.lang.String' to required type 'long'" -- so this keys on the parts common to
# both. The rejected value is quoted, and those quotes are backslash-escaped inside a JSON error
# body, hence the optional backslashes.
#
# The fragments must all come from ONE message, so the gaps exclude '"' rather than using a lazy
# '.*?' with re.DOTALL: the error body is a JSON array of messages, and an unbounded gap would
# happily splice a "Failed to convert" from one entry onto a "For input string" from another,
# blaming a perfectly valid id for an unrelated failure.
_NUMERIC_CONVERSION_FAILURE = re.compile(
    r"Failed to convert value of type[^\"]*?"
    r"(?:required type '(?:long|int)'|NumberFormatException)[^\"]*?"
    r'For input string: \\?"(.*?)\\?"'
)

# Names INCEpTION uses for the path variables it binds, mapped to the pycaprio argument they came
# from. When the server reports which parameter it was converting, that beats guessing from values.
_SERVER_PARAMETER_NAMES = {"projectId": "project", "documentId": "document"}
_REPORTED_PARAMETER = re.compile(r"Method parameter '(\w+)'")

# Listing call that yields the ids for a given parameter, so the error can point somewhere useful.
_LOOKUP_HINTS = {"project": "client.api.projects()", "document": "client.api.documents(project)"}


def _translate_exception(
    bad_response_error: InceptionBadResponse,
    project: Optional[Union[int, str]] = None,
    document: Optional[Union[int, str]] = None,
) -> Optional[IllegalIdentifier]:
    """
    Turns INCEpTION's opaque "failed to parse a long" HTTP 500 into an ``IllegalIdentifier`` naming
    the argument whose value the server rejected, or returns ``None`` when the response is not that
    failure -- in which case the caller must let the original error through.

    ``project``/``document`` are the identifiers that went into the request. The translation is
    driven purely by what the server reports, so it disappears on its own once INCEpTION resolves
    projects by slug: the parse never fails, so nothing is ever translated.
    """
    response_text = bad_response_error.bad_response.text
    match = _NUMERIC_CONVERSION_FAILURE.search(response_text)
    if match is None:
        return None
    rejected = match.group(1)
    # A numeric value that still fails to parse is out of range for a Java long, not a name or slug;
    # saying "ids must be numeric" about it would be actively misleading.
    if rejected.lstrip("-").isdigit():
        return None
    # Only claim responsibility for a value we actually put into the request; an unrelated
    # NumberFormatException from deeper inside INCEpTION must keep its original error.
    candidates = [(name, value) for name, value in (("document", document), ("project", project)) if value is not None]
    # Prefer the parameter INCEpTION says it was binding; guessing from the value alone misattributes
    # the error when both identifiers are the same string. Older versions report no parameter name,
    # so fall back to matching by value -- document-first, as the more specific culprit when a
    # request carries both.
    reported = _REPORTED_PARAMETER.search(response_text)
    preferred = _SERVER_PARAMETER_NAMES.get(reported.group(1)) if reported else None
    if preferred:
        candidates.sort(key=lambda candidate: candidate[0] != preferred)
    for parameter_name, identifier in candidates:
        if str(identifier) == rejected:
            return IllegalIdentifier(
                bad_response_error.bad_response, parameter_name, identifier, _LOOKUP_HINTS.get(parameter_name)
            )
    return None


class HttpInceptionAdapter(BaseInceptionAdapter):
    """
    Adapter which connects to the INCEpTION's API.
    Documentation is described in the 'BaseInceptionAdapter' class.
    """

    def __init__(
        self,
        inception_host: str,
        authentication: authentication_type,
        inception_client: Optional[BaseInceptionClient] = None,
        ca_bundle: Optional[str] = None,
        verify: Union[bool, str] = True,
    ):
        self.client = inception_client or RetryableInceptionClient(
            inception_host, authentication, ca_bundle=ca_bundle, verify=verify
        )
        self.default_username, _ = authentication

    def _request(
        self,
        verb: str,
        url: str,
        project: Optional[Union[int, str]] = None,
        document: Optional[Union[int, str]] = None,
        **kwargs,
    ):
        """
        Performs a request, replacing INCEpTION's opaque "failed to parse a long" HTTP 500 with an
        ``IllegalIdentifier`` naming the argument the rejected value came from. The identifiers
        passed here are the ones interpolated into ``url``. See ``_translate_exception``.
        """
        try:
            return getattr(self.client, verb)(url, **kwargs)
        except InceptionBadResponse as bad_response_error:
            translated = _translate_exception(bad_response_error, project=project, document=document)
            if translated is not None:
                raise translated from bad_response_error
            raise

    def projects(self) -> List[Project]:
        response = self.client.get("/projects")
        return ProjectSchema().load(response.json()["body"], many=True)

    def project(self, project: Union[Project, int, str]) -> Project:
        project_id = self._get_object_id(project)
        response = self._request("get", f"/projects/{project_id}", project=project_id)
        return ProjectSchema().load(response.json()["body"], many=False)

    def documents(self, project: Union[Project, int, str]) -> List[Document]:
        project_id = self._get_object_id(project)
        response = self._request("get", f"/projects/{project_id}/documents", project=project_id)
        document_list = DocumentSchema().load(response.json()["body"], many=True)
        for document in document_list:
            document.project_id = project_id
        return document_list

    def document(
        self,
        project: Union[Project, int, str],
        document: Union[Document, int, str],
        document_format: str = InceptionFormat.DEFAULT,
    ) -> bytes:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self._request(
            "get",
            f"/projects/{project_id}/documents/{document_id}",
            project=project_id,
            document=document_id,
            params={"format": document_format},
        )
        return response.content

    def annotations(self, project: Union[Project, int, str], document: Union[Document, int, str]) -> List[Annotation]:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self._request(
            "get",
            f"/projects/{project_id}/documents/{document_id}/annotations",
            project=project_id,
            document=document_id,
        )
        annotation_list = AnnotationSchema().load(response.json()["body"], many=True)
        for annotation in annotation_list:
            annotation.project_id = project_id
            annotation.document_id = document_id
        return annotation_list

    def annotation(
        self,
        project: Union[Project, int, str],
        document: Union[Document, int, str],
        user_name: str,
        annotation_format: str = InceptionFormat.DEFAULT,
    ) -> bytes:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self._request(
            "get",
            f"/projects/{project_id}/documents/{document_id}/annotations/{self._quote_segment(user_name)}",
            project=project_id,
            document=document_id,
            params={"format": annotation_format},
        )
        return response.content

    def create_project(
        self, project_name: str, project_title: Optional[str] = None, creator_name: Optional[str] = None
    ) -> Project:
        creator_name = creator_name or self.default_username
        project_title = project_title or project_name
        response = self.client.post(
            "/projects", data={"creator": creator_name, "name": project_name, "title": project_title}
        )
        return ProjectSchema().load(response.json()["body"])

    def create_document(
        self,
        project: Union[Project, int, str],
        document_name: str,
        content: IO,
        document_format: str = InceptionFormat.DEFAULT,
        document_state: str = DocumentState.DEFAULT,
        filename: Optional[str] = None,
    ) -> Document:
        project_id = self._get_object_id(project)
        response = self._request(
            "post",
            f"/projects/{project_id}/documents",
            project=project_id,
            form_data={"name": document_name, "format": document_format, "state": document_state},
            files={"content": (_resolve_document_filename(content, filename), content)},
        )
        document = DocumentSchema().load(response.json()["body"], many=False)
        document.project_id = project_id
        return document

    def create_annotation(
        self,
        project: Union[Project, int, str],
        document: Union[Document, int, str],
        user_name: str,
        content: IO,
        annotation_format: str = InceptionFormat.DEFAULT,
        annotation_state: str = AnnotationState.DEFAULT,
    ) -> Annotation:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self._request(
            "post",
            f"/projects/{project_id}/documents/{document_id}/annotations/{self._quote_segment(user_name)}",
            project=project_id,
            document=document_id,
            form_data={"format": annotation_format, "state": annotation_state},
            files={"content": ("data", content)},
        )
        annotation = AnnotationSchema().load(response.json()["body"], many=False)
        annotation.project_id = project_id
        annotation.document_id = document_id
        return annotation

    def update_annotation_state(
        self,
        project: Union[Project, int, str],
        document: Union[Document, int, str],
        user_name: str,
        annotation_state: str,
    ) -> bool:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)

        self._request(
            "post",
            f"/projects/{project_id}/documents/{document_id}/annotations/{self._quote_segment(user_name)}/state",
            project=project_id,
            document=document_id,
            form_data={"state": annotation_state},
        )
        return True

    def delete_project(self, project: Union[Project, int, str]) -> bool:
        project_id = self._get_object_id(project)
        self._request("delete", f"/projects/{project_id}", project=project_id)
        return True

    def delete_document(self, project: Union[Project, int, str], document: Union[Document, int, str]) -> bool:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        self._request(
            "delete", f"/projects/{project_id}/documents/{document_id}", project=project_id, document=document_id
        )
        return True

    def delete_annotation(
        self, project: Union[Project, int, str], document: Union[Document, int, str], user_name: str
    ) -> bool:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        self._request(
            "delete",
            f"/projects/{project_id}/documents/{document_id}/annotations/{self._quote_segment(user_name)}",
            project=project_id,
            document=document_id,
        )
        return True

    def export_project(self, project: Union[Project, int, str], project_format: str = InceptionFormat.DEFAULT) -> bytes:
        project_id = self._get_object_id(project)
        response = self._request(
            "get", f"/projects/{project_id}/export.zip", project=project_id, params={"format": project_format}
        )
        return response.content

    def import_project(self, zip_file: IO) -> Project:
        response = self.client.post("/projects/import", files={"file": ("data", zip_file)})
        return ProjectSchema().load(response.json()["body"], many=False)

    def curations(
        self, project: Union[Project, int, str], document_state: str = InceptionFormat.DEFAULT
    ) -> List[Document]:
        curations_list = self.documents(project)
        curator_list = [document for document in curations_list if document.document_state == document_state]
        return curator_list

    def curation(
        self,
        project: Union[Project, int, str],
        document: Union[Document, int, str],
        curation_format: str = InceptionFormat.DEFAULT,
    ) -> bytes:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self._request(
            "get",
            f"/projects/{project_id}/documents/{document_id}/curation",
            project=project_id,
            document=document_id,
            params={"format": curation_format},
        )
        return response.content

    def create_curation(
        self,
        project: Union[Project, int, str],
        document: Union[Document, int, str],
        content: IO,
        document_state: str = DocumentState.CURATION_IN_PROGRESS,
        curation_format: str = InceptionFormat.DEFAULT,
    ) -> Curation:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self._request(
            "post",
            f"/projects/{project_id}/documents/{document_id}/curation",
            project=project_id,
            document=document_id,
            form_data={"format": curation_format, "state": document_state},
            files={"content": ("data", content)},
        )
        curation = CurationSchema().load(response.json()["body"], many=False)
        curation.project_id = project_id
        curation.document_id = document_id
        return curation

    def delete_curation(self, project: Union[Project, int, str], document: Union[Document, int, str]) -> bool:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        self._request(
            "delete",
            f"/projects/{project_id}/documents/{document_id}/curation",
            project=project_id,
            document=document_id,
        )
        return True

    def list_roles(self, project: Union[Project, int, str], user_id: str) -> List[str]:
        project_id = self._get_object_id(project)
        response = self._request(
            "get", f"/projects/{project_id}/permissions/{self._quote_segment(user_id)}", project=project_id
        )
        return self._extract_role_names(response)

    def assign_roles(self, project: Union[Project, int, str], user_id: str, roles: List[str]) -> List[str]:
        if not roles:
            raise ValueError("roles must not be empty; provide at least one role to assign")
        project_id = self._get_object_id(project)
        response = self._request(
            "post",
            f"/projects/{project_id}/permissions/{self._quote_segment(user_id)}",
            project=project_id,
            params={"roles": roles},
        )
        return self._extract_role_names(response)

    def delete_roles(self, project: Union[Project, int, str], user_id: str, roles: List[str]) -> List[str]:
        if not roles:
            raise ValueError("roles must not be empty; provide at least one role to delete")
        project_id = self._get_object_id(project)
        response = self._request(
            "delete",
            f"/projects/{project_id}/permissions/{self._quote_segment(user_id)}",
            project=project_id,
            params={"roles": roles},
        )
        return self._extract_role_names(response)

    @staticmethod
    def _extract_role_names(response) -> List[str]:
        """
        Parses a permissions response into a list of role names. A mutating endpoint (assign/delete)
        may answer with an empty/no-content body, which is treated as "no roles" rather than raising.
        """
        if not response.content:
            return []
        return [permission["role"] for permission in response.json()["body"]]

    @staticmethod
    def _quote_segment(segment: Union[int, str]) -> str:
        """
        URL-encodes a single path segment so that user-controlled values (e.g. usernames
        containing '/', spaces or other reserved characters) do not corrupt the request path.
        """
        return quote(str(segment), safe="")

    @staticmethod
    def _get_object_id(o: Union[int, str, Project, Document, Annotation]) -> Union[int, str]:
        if isinstance(o, Project):
            return o.project_id
        if isinstance(o, Document):
            return o.document_id
        if isinstance(o, Annotation):
            return o.user_name

        # If it is an unknown type (e.g. a raw int/str id), just return it.
        return o
