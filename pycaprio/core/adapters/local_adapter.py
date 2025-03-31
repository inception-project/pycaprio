import datetime
import os
import json
import zipfile
from typing import List, Union

from pycaprio.core.interfaces.adapter import BaseInceptionAdapter
from pycaprio.core.mappings import AnnotationState, DocumentState, InceptionFormat
from pycaprio.core.objects.project import Project
from pycaprio.core.objects.document import Document
from pycaprio.core.objects.annotation import Annotation


class LocalInceptionAdapter(BaseInceptionAdapter):
    """
    Adapter for handling local INCEpTION projects stored as ZIP files.
    """

    def __init__(self, local_projects_dir: str):
        """
        Initializes the adapter with a directory containing ZIP files of exported INCEpTION projects.

        :param local_projects_dir: Directory containing exported INCEpTION projects in ZIP format.
        """
        self.local_projects_dir = local_projects_dir

    def _get_project_zip_path(self, project_id: str) -> str:
        """
        Finds the ZIP file associated with a given project ID.

        :param project_id: ID of the project. The ID is the filename of the exported project ZIP file.
        """
        zip_path = os.path.join(self.local_projects_dir, f"{project_id}.zip")
        if os.path.exists(zip_path):
            return zip_path
        raise FileNotFoundError(f"No ZIP file found for project: {project_id}")

    def projects(self) -> List[Project]:
        """
        Returns a list of all available projects (metadata) in the local directory.
        """
        projects = []
        zip_files = [f for f in os.listdir(self.local_projects_dir) if f.endswith(".zip")]
        for zip_file in zip_files:
            zip_path = os.path.join(self.local_projects_dir, zip_file)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                if "exportedproject.json" in zip_ref.namelist():
                    with zip_ref.open("exportedproject.json") as json_file:
                        project_data = json.load(json_file)
                        projects.append(
                            Project(
                                project_id=zip_file.removesuffix(".zip"),
                                # If you're wondering why slug is name and name is title, it's because the INCEpTION API does it that way, so we're following that convention ¯\_(ツ)_/¯
                                project_name=project_data["slug"],
                                project_title=project_data["name"],
                            )
                        )

        return projects

    def project(self, project: Union[Project, str]) -> Project:
        """
        Returns a project (metadata).

        :param project: Project object or project ID. (Project ID is the filename of the exported project ZIP file.)
        """
        project_id = project if isinstance(project, str) else project.project_id
        zip_path = self._get_project_zip_path(project_id)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            with zip_ref.open("exportedproject.json") as json_file:
                project_data = json.load(json_file)
                return Project(
                    project_id=project_id, project_name=project_data["slug"], project_title=project_data["name"]
                )

    def documents(self, project: Union[Project, str]) -> List[str]:
        """
        Returns a list of all available documents in the project.

        :param project: Project object or project ID. (Project ID is the filename of the exported project ZIP file.)
        """
        project_id = project if isinstance(project, str) else project.project_id
        zip_path = self._get_project_zip_path(project_id)
        document_list = []
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            with zip_ref.open("exportedproject.json") as json_file:
                project_data = json.load(json_file)
                for document in project_data["source_documents"]:
                    document_list.append(
                        Document(
                            project_id=project_id,
                            document_id=document["name"],
                            document_name=document["name"],
                            document_state=document["state"],
                        )
                    )

        return document_list

    def document(self, project: Union[Project, str], document: Union[Document, str]) -> bytes:
        """
        Returns the content of a document.

        :param project: Project object or project ID. (Project ID is the filename of the exported project ZIP file.)
        :param document: Document object or document ID. (Document ID is the filename of the document in the ZIP file.)
        """

        project_id = project if isinstance(project, str) else project.project_id
        document_id = document if isinstance(document, str) else document.document_id
        zip_path = self._get_project_zip_path(project_id)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            with zip_ref.open(f"source/{document_id}") as document_file:
                return document_file.read()

    def annotations(self, project: Union[Project, str], document: Union[Document, str]) -> List[Annotation]:
        """
        Returns a list of all annotations for a document.

        :param project: Project object or project ID. (Project ID is the filename of the exported project ZIP file.)
        :param document: Document object or document ID. (Document ID is the filename of the document in the ZIP file.)
        """
        project_id = project if isinstance(project, str) else project.project_id
        document_id = document if isinstance(document, str) else document.document_id
        zip_path = self._get_project_zip_path(project_id)
        annotation_list = []
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            with zip_ref.open("exportedproject.json") as json_file:
                project_data = json.load(json_file)
                for d in project_data["annotation_documents"]:
                    if d["name"] == document_id:
                        annotation_list.append(
                            Annotation(
                                project_id=project_id,
                                document_id=document_id,
                                user_name=d["user"],
                                annotation_state=d["state"],
                                timestamp=datetime.datetime.fromtimestamp(
                                    d["timestamp"] // 1000, tz=datetime.timezone(datetime.timedelta(hours=2))
                                ),
                            )
                        )

        return annotation_list

    def annotation(self, project: Union[Project, str], document: Union[Document, str], user_name: str) -> bytes:
        """
        Returns the content of an annotation.
        NOTE: Returns the annotation in JSON CAS format only.

        :param project: Project object or project ID. (Project ID is the filename of the exported project ZIP file.)
        :param document: Document object or document ID. (Document ID is the filename of the document in the ZIP file.)
        :param user_name: User name of the annotator.
        """

        project_id = project if isinstance(project, str) else project.project_id
        document_id = document if isinstance(document, str) else document.document_id
        zip_path = self._get_project_zip_path(project_id)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            with zip_ref.open(f"annotation/{document_id}/{user_name}.json") as document_file:
                return document_file.read()

    def create_project(self, project_name, creator_name):
        raise NotImplementedError

    def create_document(
        self,
        project,
        document_name,
        content,
        document_format=InceptionFormat.DEFAULT,
        document_state=DocumentState.DEFAULT,
    ):
        raise NotImplementedError

    def create_annotation(
        self,
        project,
        document,
        user_name,
        content,
        annotation_format=InceptionFormat.DEFAULT,
        annotation_state=AnnotationState.DEFAULT,
    ):
        raise NotImplementedError

    def update_annotation_state(self, project, document, user_name, annotation_state):
        raise NotImplementedError

    def delete_project(self, project):
        raise NotImplementedError

    def delete_document(self, project, document):
        raise NotImplementedError

    def delete_annotation(self, project, document, user_name):
        raise NotImplementedError

    def export_project(self, project, project_format=InceptionFormat.DEFAULT):
        raise NotImplementedError

    def import_project(self, zip_file):
        raise NotImplementedError

    def create_curation(
        self, project, document, content, document_state=DocumentState.DEFAULT, curation_format=InceptionFormat.DEFAULT
    ):
        raise NotImplementedError

    def curations(self, project, document_state=InceptionFormat.DEFAULT):
        raise NotImplementedError

    def curation(self, project, document, curation_format=InceptionFormat.DEFAULT):
        raise NotImplementedError

    def delete_curation(self, project, document):
        raise NotImplementedError
