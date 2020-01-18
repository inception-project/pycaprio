from typing import IO, Union
from typing import List
from typing import Optional

from pycaprio.core.clients.retryable_client import RetryableInceptionClient
from pycaprio.core.interfaces.adapter import BaseInceptionAdapter
from pycaprio.core.interfaces.types import authentication_type
from pycaprio.core.mappings import AnnotationState
from pycaprio.core.mappings import InceptionFormat
from pycaprio.core.mappings import DocumentState
from pycaprio.core.objects.annotation import Annotation
from pycaprio.core.objects.document import Document
from pycaprio.core.objects.project import Project
from pycaprio.core.schemas.annotation import AnnotationSchema
from pycaprio.core.schemas.document import DocumentSchema
from pycaprio.core.schemas.project import ProjectSchema


class HttpInceptionAdapter(BaseInceptionAdapter):
    """
    Adapter which connects to the INCEpTION's API.
    Documentation is described in the 'BaseInceptionAdapter' class.
    """

    def __init__(self, inception_host: str, authentication: authentication_type):
        self.client = RetryableInceptionClient(inception_host, authentication)
        self.default_username, _ = authentication

    def projects(self) -> List[Project]:
        response = self.client.get('/projects', allowed_statuses=(200,))
        return ProjectSchema().load(response.json()['body'], many=True)

    def project(self, project: Union[Project, int]) -> Project:
        project_id = self._get_object_id(project)
        response = self.client.get(f'/projects/{project_id}')
        return ProjectSchema().load(response.json()['body'], many=False)

    def documents(self, project: Union[Project, int]) -> List[Document]:
        project_id = self._get_object_id(project)
        response = self.client.get(f'/projects/{project_id}/documents', allowed_statuses=(200,))
        document_list = DocumentSchema().load(response.json()['body'], many=True)
        for document in document_list:
            document.project_id = project_id
        return document_list

    def document(self, project: Union[Project, int], document: Union[Document, int],
                 document_format: str = InceptionFormat.DEFAULT) -> bytes:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self.client.get(f'/projects/{project_id}/documents/{document_id}', allowed_statuses=(200,),
                                   params={'format': document_format})
        return response.content

    def annotations(self, project: Union[Project, int], document: Union[Document, int]) -> List[Annotation]:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self.client.get(f'/projects/{project_id}/documents/{document_id}/annotations',
                                   allowed_statuses=(200,))
        annotation_list = AnnotationSchema().load(response.json()['body'], many=True)
        for annotation in annotation_list:
            annotation.project_id = project_id
            annotation.document_id = document_id
        return annotation_list

    def annotation(self, project: Union[Project, int], document: Union[Document, int], user_name: str,
                   annotation_format: str = InceptionFormat.DEFAULT) -> bytes:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self.client.get(f'/projects/{project_id}/documents/{document_id}/annotations/{user_name}',
                                   allowed_statuses=(200,), params={'format': annotation_format})
        return response.content

    def create_project(self, project_name: str, creator_name: Optional[str] = None) -> Project:
        creator_name = creator_name or self.default_username
        response = self.client.post('/projects', form_data={'creator': creator_name, 'name': project_name},
                                    allowed_statuses=(201,))
        return ProjectSchema().load(response.json()['body'])

    def create_document(self, project: Union[Project, int], document_name: str, content: IO,
                        document_format: str = InceptionFormat.DEFAULT,
                        document_state: str = DocumentState.DEFAULT) -> Document:
        project_id = self._get_object_id(project)
        response = self.client.post(f"/projects/{project_id}/documents", form_data={"name": document_name,
                                                                                    "format": document_format,
                                                                                    "state": document_state},
                                    files={"content": ('test/path', content)},
                                    allowed_statuses=(201, 200))
        document = DocumentSchema().load(response.json()['body'], many=False)
        document.project_id = project_id
        return document

    def create_annotation(self, project: Union[Project, int], document: Union[Document, int], user_name: str,
                          content: IO,
                          annotation_format: str = InceptionFormat.DEFAULT,
                          annotation_state: str = AnnotationState.DEFAULT) -> Annotation:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        response = self.client.post(f"/projects/{project_id}/documents/{document_id}/annotations/{user_name}",
                                    form_data={'format': annotation_format, 'state': annotation_state},
                                    files={"content": ('test/path', content)},
                                    allowed_statuses=(201, 200))
        annotation = AnnotationSchema().load(response.json()['body'], many=False)
        annotation.project_id = project_id
        annotation.document_id = document_id
        return annotation

    def delete_project(self, project: Union[Project, int]) -> bool:
        project_id = self._get_object_id(project)
        self.client.delete(f'/projects/{project_id}', allowed_statuses=(204, 200,))
        return True

    def delete_document(self, project: Union[Project, int], document: Union[Document, int]) -> bool:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        self.client.delete(f'/projects/{project_id}/documents/{document_id}', allowed_statuses=(204, 200))
        return True

    def delete_annotation(self, project: Union[Project, int], document: Union[Document, int], user_name: str) -> bool:
        project_id = self._get_object_id(project)
        document_id = self._get_object_id(document)
        self.client.delete(f'/projects/{project_id}/documents/{document_id}/annotations/{user_name}',
                           allowed_statuses=(204, 200))
        return True

    def export_project(self, project: Union[Project, int], project_format: str = InceptionFormat.DEFAULT) -> bytes:
        project_id = self._get_object_id(project)
        response = self.client.get(f"/projects/{project_id}/export.zip", allowed_statuses=(200,),
                                   params={'format': project_format})
        return response.content

    def import_project(self, zip_stream: IO) -> Project:
        response = self.client.post("/projects/import", files={"file": ('test/path', zip_stream)},
                                    allowed_statuses=(201, 200))
        return ProjectSchema().load(response.json()['body'], many=False)

    @staticmethod
    def _get_object_id(o: Union[int, Project, Document, Annotation]) -> int:
        object_id_mappings = {
            Project: lambda p: p.project_id,
            Document: lambda d: d.document_id,
            Annotation: lambda a: a.user_name
        }
        for object_class, mapper in object_id_mappings.items():
            if isinstance(o, object_class):
                return mapper(o)

        # If it is an unknown type, just return it.
        return o
