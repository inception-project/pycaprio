from pycaprio.core.mappings import AnnotationState
from pycaprio.core.objects import Annotation
from tests.integ_tests.conftest import TEST_USERNAME, TEST_CONTENT


def test_list_annotation(pycaprio, test_project, test_document, test_io):
    pycaprio.api.create_annotation(test_project, test_document, TEST_USERNAME, test_io)
    annotations = pycaprio.api.annotations(test_project, test_document)
    assert annotations
    assert all(isinstance(a, Annotation) for a in annotations)


def test_create_annotation(pycaprio, test_project, test_document, test_io):
    annotation = pycaprio.api.create_annotation(test_project, test_document, TEST_USERNAME, test_io)
    assert annotation in pycaprio.api.annotations(test_project, test_document)


def test_detail_annotation(pycaprio, test_project, test_document, test_io):
    annotation = pycaprio.api.create_annotation(test_project, test_document, TEST_USERNAME, test_io)
    assert TEST_CONTENT == pycaprio.api.annotation(test_project, test_document, annotation.user_name).decode("utf-8")


def test_delete_annotation(pycaprio, test_project, test_document, test_io):
    annotation = pycaprio.api.create_annotation(test_project, test_document, TEST_USERNAME, test_io)
    pycaprio.api.delete_annotation(test_project, test_document, annotation.user_name)
    assert annotation not in pycaprio.api.annotations(test_project, test_document)


def test_update_annotation_state(pycaprio, test_project, test_document, test_io):
    initial_annotation = pycaprio.api.create_annotation(test_project, test_document, TEST_USERNAME, test_io)
    pycaprio.api.update_annotation_state(
        test_project, test_document, initial_annotation.user_name, AnnotationState.COMPLETE
    )
    updated_annotation = [
        a for a in pycaprio.api.annotations(test_project, test_document) if a.user_name == initial_annotation.user_name
    ][0]
    assert updated_annotation.annotation_state == AnnotationState.COMPLETE
