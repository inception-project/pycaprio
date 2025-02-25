import pytest

from pycaprio.core.schemas.annotation import AnnotationSchema
from pycaprio.core.schemas.document import DocumentSchema
from pycaprio.core.schemas.project import ProjectSchema
from pycaprio.core.schemas.curation import CurationSchema


# Fixtures for project


@pytest.fixture
def project_schema():
    return ProjectSchema()


@pytest.fixture
def document_schema():
    return DocumentSchema()


@pytest.fixture
def annotation_schema():
    return AnnotationSchema()


@pytest.fixture
def curation_schema():
    return CurationSchema()
