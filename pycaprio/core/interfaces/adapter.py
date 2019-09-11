from abc import ABCMeta
from abc import abstractmethod
from typing import IO

from typing import List

from pycaprio.core.mappings import AnnotationStatus
from pycaprio.core.mappings import DocumentFormats
from pycaprio.core.mappings import DocumentStatus
from pycaprio.core.objects.annotation import Annotation
from pycaprio.core.objects.document import Document
from pycaprio.core.objects.project import Project


class BaseInceptionAdapter(metaclass=ABCMeta):

    @abstractmethod
    def projects(self) -> List[Project]:
        """
        Retrieves a list of Projects
        :return: List of Project objects
        """
        pass  # pragma: no cover

    @abstractmethod
    def project(self, project_id: int) -> Project:
        """
        Retrieves a Project
        :param project_id: Project id
        :return: Project object
        """
        pass  # pragma: no cover

    @abstractmethod
    def documents(self, project_id: int) -> List[Document]:
        """
        Retrieves a list of Documents of a Project.
        :param project_id: The project_id of the Project where the Documents are located
        :return: List of Document objects
        """
        pass  # pragma: no cover

    @abstractmethod
    def document(self, project_id: int, document_id: int) -> bytes:
        """
        Retrieves a Document
        :param project_id: The project_id of the Project where the Document is located
        :param document_id: Document id
        :return: Content of the Document in bytes
        """
        pass  # pragma: no cover

    @abstractmethod
    def annotations(self, project_id: int, document_id: int) -> List[Annotation]:
        """
        Retrieves a list of Annotations of a Document in a Project.
        :param project_id: The project_id of the Project where the Annotations are located
        :param document_id: The document_id of the Document where the Annotations are located
        :return: List of Annotation objects
        """
        pass  # pragma: no cover

    @abstractmethod
    def annotation(self, project_id: int, document_id: int, annotation_id: int,
                   format: str = DocumentFormats.DEFAULT) -> bytes:
        """
        Retrieves a Document
        :param project_id: The project_id of the Project where the Annotation is located
        :param document_id: The document_id of the Document where the Annotation is located
        :param format: Format in which the annotation will be downloaded
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
    def create_document(self, project_id: int, document_name: str, content: IO,
                        document_format: str = DocumentFormats.DEFAULT,
                        state: str = DocumentStatus.DEFAULT) -> Document:
        """
        Creates a Document
        :param project_id: Id of the Project where the new Document will be created
        :param document_name: Document name.
        :param content: Content of the Document.
        :param document_format: Document format.
        :param state: State of the Document.
        :return: Recently created Document
        """
        pass  # pragma: no cover

    @abstractmethod
    def create_annotation(self, project_id: int, document_id: int, user_name: str, content: IO,
                          annotation_format: str = DocumentFormats.DEFAULT, state: str = AnnotationStatus.DEFAULT):
        """
        Creates a Document
        :param project_id: Id of the Project where the new Document will be created
        :param document_id: Id of the Document which is targeted for annotation.
        :param user_name: Annotator's username.
        :param content: Content of the Annotation.
        :param annotation_format: Annotation format.
        :param state: State of the Annotation.
        :return: Recently created Document.
        """
        pass  # pragma: no cover

    @abstractmethod
    def delete_project(self, project_id: int) -> bool:
        """
        Deletes Project.
        :param project_id: Project id.
        """
        pass  # pragma: no cover

    @abstractmethod
    def delete_document(self, project_id: int, document_id: int) -> bool:
        """
        Deletes Document from a Project.
        :param project_id: Project id.
        :param document_id: Document id.
        """
        pass  # pragma: no cover

    @abstractmethod
    def delete_annotation(self, project_id: int, document_id: int, user_name: str) -> bool:
        """
        Deletes an Annotation from a Document in a Project
        :param project_id: Project id.
        :param document_id: Document id.
        :param user_name: Annotator's username.
        """
        pass  # pragma: no cover

    @abstractmethod
    def export_project(self, project_id: int, format: str = DocumentFormats.DEFAULT) -> bytes:
        """
        Exports a Project into a .zip file.
        :param project_id: Project id.
        :param format: Format in which the documents and annotations will be exported.
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
