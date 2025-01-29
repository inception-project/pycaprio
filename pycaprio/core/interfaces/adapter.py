from abc import ABCMeta
from abc import abstractmethod
from typing import IO, Union

from typing import List

from pycaprio.core.mappings import AnnotationState
from pycaprio.core.mappings import InceptionFormat
from pycaprio.core.mappings import DocumentState
from pycaprio.core.mappings import RoleType
from pycaprio.core.objects.annotation import Annotation
from pycaprio.core.objects.document import Document
from pycaprio.core.objects.project import Project
from pycaprio.core.objects.curation import Curation
from pycaprio.core.objects.role import RoleType


class BaseInceptionAdapter(metaclass=ABCMeta):

    @abstractmethod
    def projects(self) -> List[Project]:
        """
        Retrieves a list of Projects
        :return: List of Project objects
        """
        pass  # pragma: no cover

    @abstractmethod
    def project(self, project: Union[Project, int]) -> Project:
        """
        Retrieves a Project
        :param project: Project/Project id
        :return: Project object
        """
        pass  # pragma: no cover

    @abstractmethod
    def documents(self, project: Union[Project, int]) -> List[Document]:
        """
        Retrieves a list of Documents of a Project.
        :param project: The project/project id of the Project where the Documents are located
        :return: List of Document objects
        """
        pass  # pragma: no cover

    @abstractmethod
    def document(self, project: Union[Project, int], document: Union[Document, int],
                 document_format: str = InceptionFormat.DEFAULT) -> bytes:
        """
        Retrieves a Document
        :param project: The project/project id of the Project where the Document is located
        :param document: Document/Document id
        :param document_format: Format in which the document will be downloaded
        :return: Content of the Document in bytes
        """
        pass  # pragma: no cover

    @abstractmethod
    def annotations(self, project: Union[Project, int], document: Union[Document, int]) -> List[Annotation]:
        """
        Retrieves a list of Annotations of a Document in a Project.
        :param project: The project/project id of the Project where the Annotations are located
        :param document: The document/document id of the Document where the Annotations are located
        :return: List of Annotation objects
        """
        pass  # pragma: no cover

    @abstractmethod
    def annotation(self, project: Union[Project, int], document: Union[Document, int],
                   annotation: Union[int, Annotation],
                   annotation_format: str = InceptionFormat.DEFAULT) -> bytes:
        """
        Retrieves a Document
        :param project: The project/project id of the Project where the Annotation is located
        :param document: The document/document_id of the Document where the Annotation is located
        :param annotation: The annotation/annotation's id
        :param annotation_format: Format in which the annotation will be downloaded
        :return: Content of the Annotation in bytes
        """
        pass  # pragma: no cover

    @abstractmethod
    def create_project(self, project_name: str, creator_name: str) -> Project:
        """
        Creates a Project
        :param project_name: Name of the project. Must be unique.
        :param creator_name: Username of the user which is going to create the project.
        Default's to the authenticated user.
        :return: Recently created Project
        """
        pass  # pragma: no cover

    @abstractmethod
    def create_document(self, project: Union[Project, int], document_name: str, content: IO,
                        document_format: str = InceptionFormat.DEFAULT,
                        document_state: str = DocumentState.DEFAULT) -> Document:
        """
        Creates a Document
        :param project: Project/Id of the Project where the new Document will be created
        :param document_name: Document name.
        :param content: Content of the Document.
        :param document_format: Document format.
        :param document_state: State of the Document.
        :return: Recently created Document
        """
        pass  # pragma: no cover

    @abstractmethod
    def create_annotation(self, project: Union[Project, int], document: Union[Document, int], user_name: str,
                          content: IO,
                          annotation_format: str = InceptionFormat.DEFAULT,
                          annotation_state: str = AnnotationState.DEFAULT):
        """
        Creates a Document
        :param project: Project/Id of the Project where the new Document will be created
        :param document: Document/Id of the Document which is targeted for annotation.
        :param user_name: Annotator's username.
        :param content: Content of the Annotation.
        :param annotation_format: Annotation format.
        :param annotation_state: State of the Annotation.
        :return: Recently created Document.
        """
        pass  # pragma: no cover

    @abstractmethod
    def update_annotation_state(self, project: Union[Project, int], document: Union[Document, int], user_name: str,
                                annotation_state: str) -> bool:
        """
        Updates the state of an annotation
        :param project: Project/Id of the Project where the Annotation is
        :param document: Document/Id of the Document in which the annotation is.
        :param user_name: Annotator's username.
        :param annotation_state: New state of the Annotation.
        """
        pass  # pragma: no cover

    @abstractmethod
    def delete_project(self, project: Union[Project, int]) -> bool:
        """
        Deletes Project.
        :param project: Project/Project id.
        """
        pass  # pragma: no cover

    @abstractmethod
    def delete_document(self, project: Union[Project, int], document: Union[Document, int]) -> bool:
        """
        Deletes Document from a Project.
        :param project: Project/Project id.
        :param document: Document/Document id.
        """
        pass  # pragma: no cover

    @abstractmethod
    def delete_annotation(self, project: Union[Project, int], document: Union[Document, int], user_name: str) -> bool:
        """
        Deletes an Annotation from a Document in a Project
        :param user_name: Annotator's username.
        :param project: Project/Project id.
        :param document: Document/Document id.
        """
        pass  # pragma: no cover

    @abstractmethod
    def export_project(self, project: Union[Project, int], project_format: str = InceptionFormat.DEFAULT) -> bytes:
        """
        Exports a Project into a .zip file.
        :param project: Project/Project id.
        :param project_format: Format in which the documents and annotations will be exported.
        :return: Zip file in bytes.
        """
        pass  # pragma: no cover

    @abstractmethod
    def import_project(self, zip_file: IO) -> Project:
        """
        Imports a .zip file into a Project
        :param zip_file: Zip file IO.
        :return: Project recently created.
        """
        pass  # pragma: no cover

    @abstractmethod
    def create_curation(self, project: Union[Project, int], document: Union[Document, int],
                        content: IO,
                        document_state: str = DocumentState.DEFAULT,
                        curation_format: str = InceptionFormat.DEFAULT) -> Curation:
        """
        Creates a curated Document
        :param project: Project/Id of the Project where the new Document will be created
        :param document: Document/Id of the Document in Curation.
        :param content: Content of the curated document.
        :param curation_format: Curation format.
        :param document_state: State of the Document.
        :return: Recently created Document.
        """
        pass  # pragma: no cover

    @abstractmethod
    def curations(self, project: Union[Project, int], document_state: str = InceptionFormat.DEFAULT) -> List[Document]:
        """
        Returns a list of curated documents
        :param project: Project/Project id.
        :param document_state: State of the Document.
        :return: List
        """
        pass  # pragma: no cover

    @abstractmethod
    def curation(self, project: Union[Project, int], document: Union[Document, int],
                 curation_format: str = InceptionFormat.DEFAULT) -> bytes:
        """
        Exports curated document of a Project as bytes format
        :param document: Document/Id of the Document in Curation.
        :param curation_format: Curation format.
        :param project: Project/Project id.
        :return: bytes
        """
        pass  # pragma: no cover

    @abstractmethod
    def delete_curation(self, project: Union[Project, int], document: Union[Document, int]) -> bool:
        """
        Deletes curated annotations for a document in a Project
        :param document: Document/Id of the Document in Curation.
        :param project: Project/Project id.
        """
        pass  # pragma: no cover


    @abstractmethod
    def list_roles(self, project: Union[Project, int], userId: str) -> List[RoleType]:
        """
        List permissions for a user in the given project (non AERO)
        :param project: Project/Project id.
        :param userId: Username.
        """
        pass  # pragma: no cover


    @abstractmethod
    def assign_roles(self, project: Union[Project, int], userId: str, role:List[RoleType]) -> List[RoleType]:
        """
        Assign roles to a user in the given project (non-AERO)
        :param project: Project/Project id.
        :param userId: Username.
        :param role: List of Roles [See PermissionRoles in mappings]
        """
        pass  # pragma: no cover


    @abstractmethod
    def delete_roles(self, project: Union[Project, int], userId: str, role:List[RoleType]) -> List[RoleType]:
        """
        Delete roles to a user in the given project (non-AERO)
        :param project: Project/Project id.
        :param userId: Username.
        :param role: List of Roles [See PermissionRoles in mappings]
        """
        pass  # pragma: no cover
