from typing import IO
from unittest.mock import Mock

import pytest

from pycaprio.mappings import AnnotationState
from pycaprio.core.adapters.http_adapter import HttpInceptionAdapter
from pycaprio.core.objects import Project, Document, Annotation, Curation

test_project = Project(1, "")
test_document = Document(test_project.project_id, 1, "", "")
test_annotation = Annotation(test_project.project_id, test_document.document_id, "test_user", "", None)
test_curation = Curation(test_project.project_id, test_document.document_id, "test_user", "", None)


@pytest.mark.parametrize(
    "route, verb, function, parameters",
    [
        ("/projects", "get", HttpInceptionAdapter.projects, ()),
        ("/projects/1/documents", "get", HttpInceptionAdapter.documents, (1,)),
        ("/projects/1/documents/1/annotations", "get", HttpInceptionAdapter.annotations, (1, 1)),
        ("/projects/1", "delete", HttpInceptionAdapter.delete_project, (1,)),
        ("/projects/1/documents/1", "delete", HttpInceptionAdapter.delete_document, (1, 1)),
        (
            "/projects/1/documents/1/annotations/test-username",
            "delete",
            HttpInceptionAdapter.delete_annotation,
            (1, 1, "test-username"),
        ),
        ("/projects/1/export.zip", "get", HttpInceptionAdapter.export_project, (1,)),
        ("/projects/1/documents", "get", HttpInceptionAdapter.documents, (test_project,)),
        ("/projects/1/documents/1/annotations", "get", HttpInceptionAdapter.annotations, (test_project, test_document)),
        ("/projects/1", "delete", HttpInceptionAdapter.delete_project, (test_project,)),
        ("/projects/1/documents/1", "delete", HttpInceptionAdapter.delete_document, (test_project, test_document)),
        (
            "/projects/1/documents/1/annotations/test-username",
            "delete",
            HttpInceptionAdapter.delete_annotation,
            (test_project, test_document, "test-username"),
        ),
        ("/projects/1/export.zip", "get", HttpInceptionAdapter.export_project, (test_project,)),
        ("/projects/1/export.zip", "get", HttpInceptionAdapter.export_project, (test_project,)),
        ("/projects/1/documents", "get", HttpInceptionAdapter.curations, (1,)),
        ("/projects/1/documents/1/curation", "get", HttpInceptionAdapter.curation, (1, 1)),
        ("/projects/1/documents/1/curation", "delete", HttpInceptionAdapter.delete_curation, (1, 1)),
        ("/projects/1/documents", "get", HttpInceptionAdapter.curations, (test_project,)),
        ("/projects/1/documents/1/curation", "get", HttpInceptionAdapter.curation, (test_project, test_document)),
        (
            "/projects/1/documents/1/curation",
            "delete",
            HttpInceptionAdapter.delete_curation,
            (test_project, test_document),
        ),
        (
            "/projects/1/documents/1/annotations/test-username/state",
            "post",
            HttpInceptionAdapter.update_annotation_state,
            (test_project, test_document, "test-username", AnnotationState.IN_PROGRESS),
        ),
    ],
)
def test_list_resources_gets_good_route(route, verb, function, parameters, mock_http_adapter: HttpInceptionAdapter):
    function(mock_http_adapter, *parameters)
    assert getattr(mock_http_adapter.client, verb).call_args[0][0] == route


@pytest.mark.parametrize(
    "route, verb, function, parameters",
    [
        ("/projects", "get", HttpInceptionAdapter.projects, ()),
        ("/projects/1/documents", "get", HttpInceptionAdapter.documents, (1,)),
        ("/projects/1/documents/1/annotations", "get", HttpInceptionAdapter.annotations, (1, 1)),
        ("/projects", "get", HttpInceptionAdapter.projects, ()),
        ("/projects/1/documents", "get", HttpInceptionAdapter.documents, (test_project,)),
        ("/projects/1/documents/1/annotations", "get", HttpInceptionAdapter.annotations, (test_project, test_document)),
        ("/projects/1/documents", "get", HttpInceptionAdapter.curations, (1,)),
        ("/projects/1/documents", "get", HttpInceptionAdapter.curations, (test_project,)),
    ],
)
def test_list_resources_returns_list(route, verb, function, parameters, mock_http_adapter: HttpInceptionAdapter):
    resource_list = function(mock_http_adapter, *parameters)
    assert isinstance(resource_list, list)


def test_import_project_good_url(
    mock_http_adapter: HttpInceptionAdapter, mock_io: IO, mock_http_response: Mock, serialized_project: dict
):
    mock_http_response.json.return_value = {"body": serialized_project}
    mock_http_adapter.client.post.return_value = mock_http_response
    mock_http_adapter.import_project(mock_io)
    assert mock_http_adapter.client.post.call_args[0][0] == "/projects/import"


def test_import_project_returns_project(
    mock_http_adapter: HttpInceptionAdapter, mock_io: IO, mock_http_response: Mock, serialized_project: dict
):
    mock_http_response.json.return_value = {"body": serialized_project}
    mock_http_adapter.client.post.return_value = mock_http_response
    project = mock_http_adapter.import_project(mock_io)
    assert isinstance(project, Project)


@pytest.mark.parametrize(
    "route, function, params, resource",
    [
        ("/projects/1", HttpInceptionAdapter.project, (1,), "project"),
        ("/projects/1/documents/1", HttpInceptionAdapter.document, (1, 1), "document"),
        (
            "/projects/1/documents/1/annotations/test-user",
            HttpInceptionAdapter.annotation,
            (1, 1, "test-user"),
            "annotation",
        ),
        ("/projects/1", HttpInceptionAdapter.project, (test_project,), "project"),
        ("/projects/1/documents/1", HttpInceptionAdapter.document, (test_project, test_document), "document"),
        (
            "/projects/1/documents/1/annotations/test-user",
            HttpInceptionAdapter.annotation,
            (test_project, test_document, "test-user"),
            "annotation",
        ),
        ("/projects/1/documents/1/curation", HttpInceptionAdapter.curation, (1, 1), "curation"),
        ("/projects/1/documents/1/curation", HttpInceptionAdapter.curation, (test_project, test_document), "curation"),
    ],
)
def test_get_single_resource_route_ok(
    route: str,
    function: callable,
    params: tuple,
    resource: dict,
    mock_http_adapter: HttpInceptionAdapter,
    mock_http_response: Mock,
    serializations: dict,
):
    mock_http_response.json.return_value = {"body": serializations[resource]}
    mock_http_adapter.client.get.return_value = mock_http_response
    function(mock_http_adapter, *params)
    assert mock_http_adapter.client.get.call_args[0][0] == route


def test_get_project_returns_good_instance(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_project: dict
):
    mock_http_response.json.return_value = {"body": serialized_project}
    mock_http_adapter.client.get.return_value = mock_http_response
    response = mock_http_adapter.project(1)
    assert isinstance(response, Project)


@pytest.mark.parametrize(
    "function, params",
    [
        ("document", (1, 1)),
        ("annotation", (1, 1, "test-username")),
        ("document", (test_project, test_document)),
        ("annotation", (test_project, test_document, "test-username")),
        ("curation", (1, 1)),
        ("curation", (test_project, test_document)),
    ],
)
def test_resource_returns_bytes(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, function: str, params: tuple
):
    mock_http_response.content = bytes()
    mock_http_adapter.client.get.return_value = mock_http_response
    response = getattr(HttpInceptionAdapter, function)(mock_http_adapter, *params)
    assert isinstance(response, bytes)


@pytest.mark.parametrize(
    "route, function, params, resource",
    [
        ("/projects", HttpInceptionAdapter.create_project, ("name", "creator"), "project"),
        (
            "/projects/1/documents",
            HttpInceptionAdapter.create_document,
            (
                1,
                "test-name",
                None,
            ),
            "document",
        ),
        (
            "/projects/1/documents/1/annotations/test-user",
            HttpInceptionAdapter.create_annotation,
            (
                1,
                1,
                "test-user",
                None,
            ),
            "annotation",
        ),
        (
            "/projects/1/documents",
            HttpInceptionAdapter.create_document,
            (
                test_project,
                "test-name",
                None,
            ),
            "document",
        ),
        (
            "/projects/1/documents/1/annotations/test-user",
            HttpInceptionAdapter.create_annotation,
            (
                test_project,
                test_document,
                "test-user",
                None,
            ),
            "annotation",
        ),
        (
            "/projects/1/documents/1/curation",
            HttpInceptionAdapter.create_curation,
            (
                1,
                1,
                None,
            ),
            "annotation",
        ),
        (
            "/projects/1/documents/1/curation",
            HttpInceptionAdapter.create_curation,
            (
                test_project,
                test_document,
                None,
            ),
            "annotation",
        ),
    ],
)
def test_resource_creation_good_route(
    route: str,
    function: callable,
    params: tuple,
    resource: str,
    mock_http_adapter: HttpInceptionAdapter,
    mock_http_response: Mock,
    serializations: dict,
):
    mock_http_response.json.return_value = {"body": serializations[resource]}
    mock_http_adapter.client.post.return_value = mock_http_response
    function(mock_http_adapter, *params)
    assert mock_http_adapter.client.post.call_args[0][0] == route


@pytest.mark.parametrize(
    "route, function, params, resource",
    [
        ("/projects", HttpInceptionAdapter.create_project, ("name", "creator"), "project"),
        (
            "/projects/1/documents",
            HttpInceptionAdapter.create_document,
            (
                1,
                "test-name",
                None,
            ),
            "document",
        ),
        (
            "/projects/1/documents/1/annotations/test-user",
            HttpInceptionAdapter.create_annotation,
            (
                1,
                1,
                "test-user",
                None,
            ),
            "annotation",
        ),
        (
            "/projects/1/documents",
            HttpInceptionAdapter.create_document,
            (
                test_project,
                "test-name",
                None,
            ),
            "document",
        ),
        (
            "/projects/1/documents/1/annotations/test-user",
            HttpInceptionAdapter.create_annotation,
            (
                test_project,
                test_document,
                "test-user",
                None,
            ),
            "annotation",
        ),
        (
            "/projects/1/documents/1/curation",
            HttpInceptionAdapter.create_curation,
            (test_project, test_document, "document_state", "curation_format"),
            "curation",
        ),
    ],
)
def test_resource_creation_returns_resource_instance(
    route: str,
    function: callable,
    params: tuple,
    resource: str,
    mock_http_adapter: HttpInceptionAdapter,
    mock_http_response: Mock,
    serializations: dict,
    deserializations: dict,
):
    mock_http_response.json.return_value = {"body": serializations[resource]}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = function(mock_http_adapter, *params)
    assert isinstance(response, deserializations[resource].__class__)


def test_document_has_project_id_injected_document_list(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_document: dict
):
    test_project_id = 1
    mock_http_response.json.return_value = {"body": [serialized_document]}
    mock_http_adapter.client.get.return_value = mock_http_response
    response = mock_http_adapter.documents(test_project_id)
    assert response[0].project_id == test_project_id


def test_document_has_project_id_injected_creation(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_document: dict
):
    test_project_id = 1
    mock_http_response.json.return_value = {"body": serialized_document}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = mock_http_adapter.create_document(test_project_id, "test-name", None)
    assert response.project_id == test_project_id


def test_annotation_has_project_id_injected_annotation_list(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_annotation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": [serialized_annotation]}
    mock_http_adapter.client.get.return_value = mock_http_response
    response = mock_http_adapter.annotations(test_project_id, test_document_id)
    assert response[0].project_id == test_project_id


def test_annotation_has_document_id_injected_annotation_list(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_annotation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": [serialized_annotation]}
    mock_http_adapter.client.get.return_value = mock_http_response
    response = mock_http_adapter.annotations(test_project_id, test_document_id)
    assert response[0].document_id == test_document_id


def test_annotation_has_project_id_injected_creation(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_annotation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": serialized_annotation}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = mock_http_adapter.create_annotation(test_project_id, test_document_id, "test-name", None)
    assert response.project_id == test_project_id


def test_annotation_has_document_id_injected_creation(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_annotation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": serialized_annotation}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = mock_http_adapter.create_annotation(test_project_id, test_document_id, "test-name", None)
    assert response.document_id == test_document_id


def test_curation_has_project_id_injected_creation(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_curation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": serialized_curation}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = mock_http_adapter.create_curation(test_project_id, test_document_id, "test-state", "test-format")
    assert response.project_id == test_project_id


def test_curation_has_document_id_injected_creation(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_curation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": serialized_curation}
    mock_http_adapter.client.post.return_value = mock_http_response
    response = mock_http_adapter.create_curation(test_project_id, test_document_id, "test-state", "test-format")
    assert response.document_id == test_document_id


@pytest.mark.parametrize(
    "function, params, resource",
    [
        (HttpInceptionAdapter.create_document, (1, "test-name"), "document"),
        (HttpInceptionAdapter.create_annotation, (1, 1, "test-user"), "annotation"),
        (HttpInceptionAdapter.create_curation, (1, 1), "curation"),
    ],
)
def test_content_upload_passes_content_as_named_file_tuple(
    function,
    params,
    resource,
    mock_http_adapter: HttpInceptionAdapter,
    mock_http_response: Mock,
    serializations: dict,
    mock_io: IO,
):
    # The client's _request unpacks every files value as a (name, stream) tuple, so all content
    # uploads must pass files={"content": (name, stream)} rather than a bare stream.
    mock_http_response.json.return_value = {"body": serializations[resource]}
    mock_http_adapter.client.post.return_value = mock_http_response
    function(mock_http_adapter, *params, mock_io)
    content = mock_http_adapter.client.post.call_args.kwargs["files"]["content"]
    _, stream = content
    assert stream is mock_io


@pytest.mark.parametrize(
    "value, expected_value",
    [
        (1, 1),
        (test_project, test_project.project_id),
        (test_document, test_document.document_id),
        (test_annotation, test_annotation.user_name),
        (Exception, Exception),
    ],
)
def test_get_object_id_value_ok(mock_http_adapter, value, expected_value):
    assert mock_http_adapter._get_object_id(value) == expected_value


@pytest.mark.parametrize(
    "route, verb, function, parameters",
    [
        ("/projects/1/permissions/test-user", "get", HttpInceptionAdapter.list_roles, (1, "test-user")),
        ("/projects/1/permissions/test-user", "get", HttpInceptionAdapter.list_roles, (test_project, "test-user")),
        (
            "/projects/1/permissions/test-user",
            "post",
            HttpInceptionAdapter.assign_roles,
            (1, "test-user", ["MANAGER"]),
        ),
        (
            "/projects/1/permissions/test-user",
            "delete",
            HttpInceptionAdapter.delete_roles,
            (test_project, "test-user", ["MANAGER"]),
        ),
    ],
)
def test_role_methods_good_route(route, verb, function, parameters, mock_http_adapter: HttpInceptionAdapter):
    function(mock_http_adapter, *parameters)
    assert getattr(mock_http_adapter.client, verb).call_args[0][0] == route


@pytest.mark.parametrize(
    "function, parameters",
    [
        (HttpInceptionAdapter.list_roles, (1, "test-user")),
        (HttpInceptionAdapter.assign_roles, (1, "test-user", ["MANAGER"])),
        (HttpInceptionAdapter.delete_roles, (1, "test-user", ["MANAGER"])),
    ],
)
def test_role_methods_return_list(function, parameters, mock_http_adapter: HttpInceptionAdapter):
    assert isinstance(function(mock_http_adapter, *parameters), list)


def test_list_roles_returns_role_names(mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock):
    mock_http_response.json.return_value = {"body": [{"role": "MANAGER"}, {"role": "CURATOR"}]}
    mock_http_adapter.client.get.return_value = mock_http_response
    assert mock_http_adapter.list_roles(1, "test-user") == ["MANAGER", "CURATOR"]


def test_role_methods_tolerate_empty_response_body(mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock):
    # A mutating permission endpoint may answer with no content; that must yield [] rather than
    # a JSONDecodeError from response.json() on an empty body.
    mock_http_response.content = b""
    mock_http_response.json.side_effect = ValueError("No JSON object could be decoded")
    mock_http_adapter.client.delete.return_value = mock_http_response
    assert mock_http_adapter.delete_roles(1, "test-user", ["MANAGER"]) == []


def test_assign_roles_passes_roles_as_query_params(mock_http_adapter: HttpInceptionAdapter):
    # The API reads 'roles' as a query parameter, so it must be sent via params, not the form body.
    mock_http_adapter.assign_roles(1, "test-user", ["MANAGER", "CURATOR"])
    call = mock_http_adapter.client.post.call_args
    assert call.kwargs.get("params") == {"roles": ["MANAGER", "CURATOR"]}
    assert call.kwargs.get("data") is None


def test_delete_roles_passes_roles_as_query_params(mock_http_adapter: HttpInceptionAdapter):
    mock_http_adapter.delete_roles(1, "test-user", ["MANAGER"])
    assert mock_http_adapter.client.delete.call_args.kwargs.get("params") == {"roles": ["MANAGER"]}


def test_role_methods_url_encode_user_id(mock_http_adapter: HttpInceptionAdapter):
    mock_http_adapter.list_roles(1, "user/with space")
    assert mock_http_adapter.client.get.call_args[0][0] == "/projects/1/permissions/user%2Fwith%20space"


def test_annotation_methods_url_encode_user_name(mock_http_adapter: HttpInceptionAdapter):
    encoded = "user%2Fwith%20space"

    mock_http_adapter.annotation(1, 1, "user/with space")
    assert mock_http_adapter.client.get.call_args[0][0] == f"/projects/1/documents/1/annotations/{encoded}"

    mock_http_adapter.delete_annotation(1, 1, "user/with space")
    assert mock_http_adapter.client.delete.call_args[0][0] == f"/projects/1/documents/1/annotations/{encoded}"

    mock_http_adapter.update_annotation_state(1, 1, "user/with space", "NEW")
    assert mock_http_adapter.client.post.call_args[0][0] == f"/projects/1/documents/1/annotations/{encoded}/state"


def test_assign_roles_empty_list_raises(mock_http_adapter: HttpInceptionAdapter):
    # An empty list would be dropped from the query string, so reject it client-side.
    with pytest.raises(ValueError):
        mock_http_adapter.assign_roles(1, "test-user", [])
    mock_http_adapter.client.post.assert_not_called()


def test_delete_roles_empty_list_raises(mock_http_adapter: HttpInceptionAdapter):
    with pytest.raises(ValueError):
        mock_http_adapter.delete_roles(1, "test-user", [])
    mock_http_adapter.client.delete.assert_not_called()
