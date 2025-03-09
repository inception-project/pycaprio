import json
import pytest
from unittest.mock import patch
from pycaprio.core.adapters.local_adapter import LocalInceptionAdapter
from pycaprio.core.objects.project import Project


@pytest.fixture
def local_adapter():
    return LocalInceptionAdapter("/tmp/inception_projects")


@pytest.fixture
def mock_project_data():
    return {"slug": "test-project", "name": "Test Project", "source_documents": [
        {"name": "doc1.txt", "state": "NEW"},
        {"name": "doc2.txt", "state": "ANNOTATION_IN_PROGRESS"},
    ]}



def test_get_project_zip_path_exists(local_adapter: LocalInceptionAdapter):
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        path = local_adapter._get_project_zip_path("test-project")
        assert path == "/tmp/inception_projects/test-project.zip"


def test_get_project_zip_path_not_exists(local_adapter: LocalInceptionAdapter):
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False
        with pytest.raises(FileNotFoundError):
            local_adapter._get_project_zip_path("non-existing")


def test_projects(local_adapter: LocalInceptionAdapter, mock_project_data: dict[str, str]):
    with patch("os.listdir") as mock_listdir, patch("zipfile.ZipFile") as mock_zipfile:
        mock_listdir.return_value = ["test-project.zip"]
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = ["exportedproject.json"]
        mock_zipfile.return_value.__enter__.return_value.open.return_value.__enter__.return_value.read.return_value = (
            json.dumps(mock_project_data)
        )

        projects = local_adapter.projects()

        assert len(projects) == 1
        assert isinstance(projects[0], Project)
        assert projects[0].project_id == "test-project"
        assert projects[0].project_name == "test-project"
        assert projects[0].project_title == "Test Project"


def test_project(local_adapter: LocalInceptionAdapter, mock_project_data: dict[str, str]):
    with patch("os.path.exists") as mock_exists, patch("zipfile.ZipFile") as mock_zipfile:
        mock_exists.return_value = True
        mock_zipfile.return_value.__enter__.return_value.open.return_value.__enter__.return_value.read.return_value = (
            json.dumps(mock_project_data)
        )

        project = local_adapter.project("test-project")

        assert isinstance(project, Project)
        assert project.project_id == "test-project"
        assert project.project_name == "test-project"
        assert project.project_title == "Test Project"


def test_project_with_project_object(local_adapter: LocalInceptionAdapter, mock_project_data: dict[str, str]):
    test_project = Project("test-project", "test-project", "Test Project")

    with patch("os.path.exists") as mock_exists, patch("zipfile.ZipFile") as mock_zipfile:
        mock_exists.return_value = True
        mock_zipfile.return_value.__enter__.return_value.open.return_value.__enter__.return_value.read.return_value = (
            json.dumps(mock_project_data)
        )

        project = local_adapter.project(test_project)

        assert isinstance(project, Project)
        assert project.project_id == "test-project"
        assert project.project_name == "test-project"
        assert project.project_title == "Test Project"


def test_documents(local_adapter: LocalInceptionAdapter, mock_project_data: dict):
    with patch("os.path.exists") as mock_exists, patch("zipfile.ZipFile") as mock_zipfile:
        mock_exists.return_value = True
        mock_zipfile.return_value.__enter__.return_value.open.return_value.__enter__.return_value.read.return_value = (
            json.dumps(mock_project_data)
        )

        documents = local_adapter.documents("test-project")

        assert len(documents) == 2
        assert documents[0].project_id == "test-project"
        assert documents[0].document_id == "doc1.txt"
        assert documents[0].document_name == "doc1.txt"
        assert documents[0].document_state == "NEW"
        assert documents[1].project_id == "test-project"
        assert documents[1].document_id == "doc2.txt"
        assert documents[1].document_name == "doc2.txt"
        assert documents[1].document_state == "ANNOTATION_IN_PROGRESS"


def test_documents_with_project_object(local_adapter: LocalInceptionAdapter, mock_project_data: dict):
    test_project = Project("test-project", "test-project", "Test Project")

    with patch("os.path.exists") as mock_exists, patch("zipfile.ZipFile") as mock_zipfile:
        mock_exists.return_value = True
        mock_zipfile.return_value.__enter__.return_value.open.return_value.__enter__.return_value.read.return_value = (
            json.dumps(mock_project_data)
        )

        documents = local_adapter.documents(test_project)

        assert len(documents) == 2
        assert all(doc.project_id == "test-project" for doc in documents)