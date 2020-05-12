from typing import IO
from unittest.mock import Mock

import pytest

from pycaprio.core.adapters.http_adapter import HttpInceptionAdapter
from pycaprio.core.objects import Project, Document, Annotation, Curation

test_project = Project(1, "")
test_document = Document(test_project.project_id, 1, "", "")
test_annotation = Annotation(test_project.project_id, test_document.document_id, "test_user", "", None)
test_curation = Curation(test_project.project_id, test_document.document_id, "test_user", "", None)


@pytest.mark.parametrize('route, verb, function, parameters', [
    ('/projects', 'get', HttpInceptionAdapter.projects, ()),
    ('/projects/1/documents', 'get', HttpInceptionAdapter.documents, (1,)),
    ('/projects/1/documents/1/annotations', 'get', HttpInceptionAdapter.annotations, (1, 1)),
    ('/projects/1', 'delete', HttpInceptionAdapter.delete_project, (1,)),
    ('/projects/1/documents/1', 'delete', HttpInceptionAdapter.delete_document, (1, 1)),
    ('/projects/1/documents/1/annotations/test-username', 'delete', HttpInceptionAdapter.delete_annotation,
     (1, 1, 'test-username')),
    ('/projects/1/export.zip', 'get', HttpInceptionAdapter.export_project, (1,)),
    ('/projects/1/documents', 'get', HttpInceptionAdapter.documents, (test_project,)),
    ('/projects/1/documents/1/annotations', 'get', HttpInceptionAdapter.annotations,
     (test_project, test_document)),
    ('/projects/1', 'delete', HttpInceptionAdapter.delete_project, (test_project,)),
    ('/projects/1/documents/1', 'delete', HttpInceptionAdapter.delete_document,
     (test_project, test_document)),
    ('/projects/1/documents/1/annotations/test-username', 'delete', HttpInceptionAdapter.delete_annotation,
     (test_project, test_document, 'test-username')),
    ('/projects/1/export.zip', 'get', HttpInceptionAdapter.export_project, (test_project,)),
    ('/projects/1/export.zip', 'get', HttpInceptionAdapter.export_project, (test_project,)),
    ('/projects/1/documents', 'get', HttpInceptionAdapter.curations, (1,)),
    ('/projects/1/documents/1/curation', 'get', HttpInceptionAdapter.curation, (1, 1)),
    ('/projects/1/documents/1/curation', 'delete', HttpInceptionAdapter.delete_curation, (1, 1)),
    ('/projects/1/documents', 'get', HttpInceptionAdapter.curations, (test_project,)),
    ('/projects/1/documents/1/curation', 'get', HttpInceptionAdapter.curation, (test_project, test_document)),
    ('/projects/1/documents/1/curation', 'delete', HttpInceptionAdapter.delete_curation, (test_project, test_document))
])
def test_list_resources_gets_good_route(route, verb, function, parameters, mock_http_adapter: HttpInceptionAdapter):
    function(mock_http_adapter, *parameters)
    assert getattr(mock_http_adapter.client, verb).call_args[0][0] == route


@pytest.mark.parametrize('route, verb, function, parameters', [
    ('/projects', 'get', HttpInceptionAdapter.projects, ()),
    ('/projects/1/documents', 'get', HttpInceptionAdapter.documents, (1,)),
    ('/projects/1/documents/1/annotations', 'get', HttpInceptionAdapter.annotations, (1, 1)),
    ('/projects', 'get', HttpInceptionAdapter.projects, ()),
    ('/projects/1/documents', 'get', HttpInceptionAdapter.documents, (test_project,)),
    ('/projects/1/documents/1/annotations', 'get', HttpInceptionAdapter.annotations, (test_project, test_document)),
    ('/projects/1/documents', 'get', HttpInceptionAdapter.curations, (1,)),
    ('/projects/1/documents', 'get', HttpInceptionAdapter.curations, (test_project,))
])
def test_list_resources_returns_list(route, verb, function, parameters, mock_http_adapter: HttpInceptionAdapter):
    resource_list = function(mock_http_adapter, *parameters)
    assert isinstance(resource_list, list)


def test_import_project_good_url(mock_http_adapter: HttpInceptionAdapter, mock_io: IO, mock_http_response: Mock,
                                 serialized_project: dict):
    mock_http_response.json.return_value = {'body': serialized_project}
    mock_http_adapter.client.post.return_value = mock_http_response
    mock_http_adapter.import_project(mock_io)
    assert mock_http_adapter.client.post.call_args[0][0] == '/projects/import'


def test_import_project_returns_project(mock_http_adapter: HttpInceptionAdapter, mock_io: IO, mock_http_response: Mock,
                                        serialized_project: dict):
    mock_http_response.json.return_value = {'body': serialized_project}
    mock_http_adapter.client.post.return_value = mock_http_response
    project = mock_http_adapter.import_project(mock_io)
    assert isinstance(project, Project)


@pytest.mark.parametrize('route, function, params, resource',
                         [('/projects/1', HttpInceptionAdapter.project, (1,), 'project'),
                          ('/projects/1/documents/1', HttpInceptionAdapter.document, (1, 1), 'document'),
                          ('/projects/1/documents/1/annotations/test-user', HttpInceptionAdapter.annotation,
                           (1, 1, 'test-user'), 'annotation'),
                          ('/projects/1', HttpInceptionAdapter.project, (test_project,), 'project'),
                          ('/projects/1/documents/1', HttpInceptionAdapter.document, (test_project, test_document),
                           'document'),
                          ('/projects/1/documents/1/annotations/test-user', HttpInceptionAdapter.annotation,
                           (test_project, test_document, 'test-user'), 'annotation'),
                          ('/projects/1/documents/1/curation', HttpInceptionAdapter.curation,
                           (1, 1), 'curation'),
                          ('/projects/1/documents/1/curation', HttpInceptionAdapter.curation,
                           (test_project, test_document), 'curation')
                          ])
def test_get_single_resource_route_ok(route: str, function: callable, params: tuple, resource: dict,
                                      mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock,
                                      serializations: dict):
    mock_http_response.json.return_value = {'body': serializations[resource]}
    mock_http_adapter.client.get.return_value = mock_http_response
    function(mock_http_adapter, *params)
    assert mock_http_adapter.client.get.call_args[0][0] == route


def test_get_project_returns_good_instance(mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock,
                                           serialized_project: dict):
    mock_http_response.json.return_value = {'body': serialized_project}
    mock_http_adapter.client.get.return_value = mock_http_response
    response = mock_http_adapter.project(1)
    assert isinstance(response, Project)


@pytest.mark.parametrize('function, params', [('document', (1, 1)),
                                              ('annotation', (1, 1, 'test-username')),
                                              ('document', (test_project, test_document)),
                                              ('annotation', (test_project, test_document, 'test-username')),
                                              ('curation', (1, 1)),
                                              ('curation', (test_project, test_document))
                                              ])
def test_resource_returns_bytes(mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, function: str,
                                params: tuple):
    mock_http_response.content = bytes()
    mock_http_adapter.client.get.return_value = mock_http_response
    response = getattr(HttpInceptionAdapter, function)(mock_http_adapter, *params)
    assert isinstance(response, bytes)


@pytest.mark.parametrize('route, function, params, resource',
                         [('/projects', HttpInceptionAdapter.create_project, ("name", "creator"), 'project'),
                          ('/projects/1/documents', HttpInceptionAdapter.create_document, (1, "test-name", None,),
                           'document'),
                          ('/projects/1/documents/1/annotations/test-user', HttpInceptionAdapter.create_annotation,
                           (1, 1, "test-user", None,), 'annotation'),
                          ('/projects/1/documents', HttpInceptionAdapter.create_document,
                           (test_project, "test-name", None,),
                           'document'),
                          ('/projects/1/documents/1/annotations/test-user', HttpInceptionAdapter.create_annotation,
                           (test_project, test_document, "test-user", None,), 'annotation'),
                          ('/projects/1/documents/1/curation', HttpInceptionAdapter.create_curation,
                           (1, 1, None,), 'annotation'),
                          ('/projects/1/documents/1/curation', HttpInceptionAdapter.create_curation,
                           (test_project, test_document, None,), 'annotation')
                          ])
def test_resource_creation_good_route(route: str, function: callable, params: tuple, resource: str,
                                      mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock,
                                      serializations: dict):
    mock_http_response.json.return_value = {'body': serializations[resource]}
    mock_http_adapter.client.post.return_value = mock_http_response
    function(mock_http_adapter, *params)
    assert mock_http_adapter.client.post.call_args[0][0] == route


@pytest.mark.parametrize('route, function, params, resource',
                         [('/projects', HttpInceptionAdapter.create_project, ("name", "creator"), 'project'),
                          ('/projects/1/documents', HttpInceptionAdapter.create_document, (1, "test-name", None,),
                           'document'),
                          ('/projects/1/documents/1/annotations/test-user', HttpInceptionAdapter.create_annotation,
                           (1, 1, "test-user", None,), 'annotation'),
                          ('/projects/1/documents', HttpInceptionAdapter.create_document,
                           (test_project, "test-name", None,),
                           'document'),
                          ('/projects/1/documents/1/annotations/test-user', HttpInceptionAdapter.create_annotation,
                           (test_project, test_document, "test-user", None,), 'annotation'),
                          ('/projects/1/documents/1/curation', HttpInceptionAdapter.create_curation,
                           (test_project, test_document, "document_state", "curation_format"), 'curation')
                          ])
def test_resource_creation_returns_resource_instance(route: str, function: callable, params: tuple, resource: str,
                                                     mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock,
                                                     serializations: dict, deserializations: dict):
    mock_http_response.json.return_value = {'body': serializations[resource]}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = function(mock_http_adapter, *params)
    assert isinstance(response, deserializations[resource].__class__)


def test_document_has_project_id_injected_document_list(mock_http_adapter: HttpInceptionAdapter,
                                                        mock_http_response: Mock, serialized_document: dict):
    test_project_id = 1
    mock_http_response.json.return_value = {'body': [serialized_document]}
    mock_http_adapter.client.get.return_value = mock_http_response
    response = mock_http_adapter.documents(test_project_id)
    assert response[0].project_id == test_project_id


def test_document_has_project_id_injected_creation(mock_http_adapter: HttpInceptionAdapter,
                                                   mock_http_response: Mock, serialized_document: dict):
    test_project_id = 1
    mock_http_response.json.return_value = {'body': serialized_document}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = mock_http_adapter.create_document(test_project_id, "test-name", None)
    assert response.project_id == test_project_id


def test_annotation_has_project_id_injected_annotation_list(mock_http_adapter: HttpInceptionAdapter,
                                                            mock_http_response: Mock, serialized_annotation: dict):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {'body': [serialized_annotation]}
    mock_http_adapter.client.get.return_value = mock_http_response
    response = mock_http_adapter.annotations(test_project_id, test_document_id)
    assert response[0].project_id == test_project_id


def test_annotation_has_document_id_injected_annotation_list(mock_http_adapter: HttpInceptionAdapter,
                                                             mock_http_response: Mock, serialized_annotation: dict):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {'body': [serialized_annotation]}
    mock_http_adapter.client.get.return_value = mock_http_response
    response = mock_http_adapter.annotations(test_project_id, test_document_id)
    assert response[0].document_id == test_document_id


def test_annotation_has_project_id_injected_creation(mock_http_adapter: HttpInceptionAdapter,
                                                     mock_http_response: Mock, serialized_annotation: dict):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {'body': serialized_annotation}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = mock_http_adapter.create_annotation(test_project_id, test_document_id, "test-name", None)
    assert response.project_id == test_project_id


def test_annotation_has_document_id_injected_creation(mock_http_adapter: HttpInceptionAdapter,
                                                      mock_http_response: Mock, serialized_annotation: dict):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {'body': serialized_annotation}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = mock_http_adapter.create_annotation(test_project_id, test_document_id, "test-name", None)
    assert response.document_id == test_document_id


def test_curation_has_project_id_injected_creation(mock_http_adapter: HttpInceptionAdapter,
                                                   mock_http_response: Mock, serialized_curation: dict):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {'body': serialized_curation}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = mock_http_adapter.create_curation(test_project_id, test_document_id, "test-state", "test-format")
    assert response.project_id == test_project_id


def test_curation_has_document_id_injected_creation(mock_http_adapter: HttpInceptionAdapter,
                                                    mock_http_response: Mock, serialized_curation: dict):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {'body': serialized_curation}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = mock_http_adapter.create_curation(test_project_id, test_document_id, "test-state", "test-format")
    assert response.document_id == test_document_id


@pytest.mark.parametrize("value, expected_value", [
    (1, 1),
    (test_project, test_project.project_id),
    (test_document, test_document.document_id),
    (test_annotation, test_annotation.user_name),
    (Exception, Exception)
])
def test_get_object_id_value_ok(mock_http_adapter, value, expected_value):
    assert mock_http_adapter._get_object_id(value) == expected_value
