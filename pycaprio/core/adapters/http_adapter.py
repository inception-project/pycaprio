from typing import IO, Union, List, Optional
from urllib.parse import quote

from pycaprio.core.clients.retryable_client import RetryableInceptionClient
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

    def projects(self) -> List[Project]:
        response = self.client.get("/projects")
        return ProjectSchema().load(response.json()["body"], many=True)

    def project(self, project: Union[Project, int, str]) -> Project:
        project_id = self._get_object_id(project)
        response = self.client.get(f"/projects/{project_id}")
        return ProjectSchema().load(response.json()["body"], many=False)

    def documents(self, project: Union[Project, int, str]) -> List[Document]:
        project_id = self._get_object_id(project)
        response = self.client.get(f"/projects/{project_id}/documents")
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
        response = self.client.get(
            f"/projects/{project_id}/documents/{document_id}", params={"format": document_format}
        )
        return response.content

    def annotations(self, project: Union[Project, int, str], document: Union[Document, int, str]) -> List[Annotation]:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self.client.get(f"/projects/{project_id}/documents/{document_id}/annotations")
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
        response = self.client.get(
            f"/projects/{project_id}/documents/{document_id}/annotations/{self._quote_segment(user_name)}",
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
    ) -> Document:
        project_id = self._get_object_id(project)
        response = self.client.post(
            f"/projects/{project_id}/documents",
            form_data={"name": document_name, "format": document_format, "state": document_state},
            files={"content": ("data", content)},
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
        response = self.client.post(
            f"/projects/{project_id}/documents/{document_id}/annotations/{self._quote_segment(user_name)}",
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

        self.client.post(
            f"/projects/{project_id}/documents/{document_id}/annotations/{self._quote_segment(user_name)}/state",
            form_data={"state": annotation_state},
        )
        return True

    def delete_project(self, project: Union[Project, int, str]) -> bool:
        project_id = self._get_object_id(project)
        self.client.delete(f"/projects/{project_id}")
        return True

    def delete_document(self, project: Union[Project, int, str], document: Union[Document, int, str]) -> bool:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        self.client.delete(f"/projects/{project_id}/documents/{document_id}")
        return True

    def delete_annotation(
        self, project: Union[Project, int, str], document: Union[Document, int, str], user_name: str
    ) -> bool:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        self.client.delete(
            f"/projects/{project_id}/documents/{document_id}/annotations/{self._quote_segment(user_name)}"
        )
        return True

    def export_project(self, project: Union[Project, int, str], project_format: str = InceptionFormat.DEFAULT) -> bytes:
        project_id = self._get_object_id(project)
        response = self.client.get(f"/projects/{project_id}/export.zip", params={"format": project_format})
        return response.content

    def import_project(self, zip_stream: IO) -> Project:
        response = self.client.post("/projects/import", files={"file": ("data", zip_stream)})
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
        response = self.client.get(
            f"/projects/{project_id}/documents/{document_id}/curation", params={"format": curation_format}
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
        response = self.client.post(
            f"/projects/{project_id}/documents/{document_id}/curation",
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
        self.client.delete(f"/projects/{project_id}/documents/{document_id}/curation")
        return True

    def list_roles(self, project: Union[Project, int, str], user_id: str) -> List[str]:
        project_id = self._get_object_id(project)
        response = self.client.get(f"/projects/{project_id}/permissions/{self._quote_segment(user_id)}")
        return self._extract_role_names(response)

    def assign_roles(self, project: Union[Project, int, str], user_id: str, roles: List[str]) -> List[str]:
        if not roles:
            raise ValueError("roles must not be empty; provide at least one role to assign")
        project_id = self._get_object_id(project)
        response = self.client.post(
            f"/projects/{project_id}/permissions/{self._quote_segment(user_id)}", params={"roles": roles}
        )
        return self._extract_role_names(response)

    def delete_roles(self, project: Union[Project, int, str], user_id: str, roles: List[str]) -> List[str]:
        if not roles:
            raise ValueError("roles must not be empty; provide at least one role to delete")
        project_id = self._get_object_id(project)
        response = self.client.delete(
            f"/projects/{project_id}/permissions/{self._quote_segment(user_id)}", params={"roles": roles}
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
        object_id_mappings = {
            Project: lambda p: p.project_id,
            Document: lambda d: d.document_id,
            Annotation: lambda a: a.user_name,
        }
        for object_class, mapper in object_id_mappings.items():
            if isinstance(o, object_class):
                return mapper(o)

        # If it is an unknown type, just return it.
        return o
