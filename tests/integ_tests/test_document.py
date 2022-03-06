from pycaprio.core.objects import Document
from tests.integ_tests.conftest import TEST_CONTENT


def test_create_document(pycaprio, test_project, test_name, test_io):
    document = pycaprio.api.create_document(test_project, test_name, test_io)
    assert document in pycaprio.api.documents(test_project)


def test_list_documents(pycaprio, test_project, test_name, test_io):
    pycaprio.api.create_document(test_project, test_name, test_io)
    documents = pycaprio.api.documents(test_project)
    assert documents
    assert all(isinstance(d, Document) for d in documents)


def test_detail_document_gives_content(pycaprio, test_project, test_name, test_io):
    document = pycaprio.api.create_document(test_project, test_name, test_io)
    assert pycaprio.api.document(test_project, document).decode('utf-8') == TEST_CONTENT


def test_delete_document(pycaprio, test_project, test_name, test_io):
    document = pycaprio.api.create_document(test_project, test_name, test_io)
    pycaprio.api.delete_document(test_project, document)
    assert document not in pycaprio.api.documents(test_project)
