import datetime
import io

import pytest

from pycaprio.core.mappings import AnnotationStatus
from pycaprio.core.mappings import DATE_FORMAT_ISO8601
from pycaprio.core.mappings import DocumentStatus
from pycaprio.core.mappings import NO_DOCUMENT
from pycaprio.core.mappings import NO_PROJECT
from pycaprio.core.objects.annotation import Annotation
from pycaprio.core.objects.document import Document
from pycaprio.core.objects.project import Project
from pycaprio.core.schemas.annotation import AnnotationSchema
from pycaprio.core.schemas.document import DocumentSchema
from pycaprio.core.schemas.project import ProjectSchema


# Fixtures for project

@pytest.fixture
def project_schema():
    return ProjectSchema()


@pytest.fixture
def mock_project_name():
    return "project-test"


@pytest.fixture
def mock_project_id():
    return 1


@pytest.fixture
def deserialized_project(mock_project_name: str, mock_project_id: int):
    return Project(mock_project_id, mock_project_name)


@pytest.fixture
def serialized_project(mock_project_name: str, mock_project_id: int):
    return {'id': mock_project_id, 'name': mock_project_name}


# Fixtures for document

@pytest.fixture
def document_schema():
    return DocumentSchema()


@pytest.fixture
def mock_document_id():
    return 1


@pytest.fixture
def mock_document_name():
    return "document-test"


@pytest.fixture
def mock_document_state():
    return DocumentStatus.DEFAULT


@pytest.fixture
def deserialized_document(mock_document_id: int, mock_document_name: str, mock_document_state: str):
    return Document(NO_PROJECT, mock_document_id, mock_document_name, mock_document_state)


@pytest.fixture
def serialized_document(mock_document_id: int, mock_document_name: str, mock_document_state: str):
    return {'id': mock_document_id, 'name': mock_document_name, 'state': mock_document_state}


# Fixtures for annotation

@pytest.fixture
def annotation_schema():
    return AnnotationSchema()


@pytest.fixture
def mock_annotation_user():
    return "test-user"


@pytest.fixture
def mock_annotation_state():
    return AnnotationStatus.DEFAULT


@pytest.fixture
def mock_str_date():
    return "2000-01-20T10:00:00+0000"


@pytest.fixture
def mock_datetime_date(mock_str_date: str):
    return datetime.datetime.strptime(mock_str_date, DATE_FORMAT_ISO8601)


@pytest.fixture
def deserialized_annotation(mock_annotation_user: str, mock_annotation_state: str,
                            mock_datetime_date: datetime.datetime):
    return Annotation(NO_PROJECT, NO_DOCUMENT, mock_annotation_user, mock_annotation_state, mock_datetime_date)


@pytest.fixture
def serialized_annotation(mock_annotation_user: str, mock_annotation_state: str, mock_str_date: str):
    return {'user': mock_annotation_user, 'state': mock_annotation_state, 'timestamp': mock_str_date}


@pytest.fixture
def mock_io():
    return io.StringIO("test-content")


@pytest.fixture
def serializations(serialized_project, serialized_annotation, serialized_document):
    return {'project': serialized_project, 'annotation': serialized_annotation, 'document': serialized_document}


@pytest.fixture
def deserializations(deserialized_project, deserialized_annotation, deserialized_document):
    return {'project': deserialized_project, 'annotation': deserialized_annotation, 'document': deserialized_document}
