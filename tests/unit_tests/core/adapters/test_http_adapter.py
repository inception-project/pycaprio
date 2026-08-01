import io
from typing import IO, Callable, cast
from unittest.mock import Mock

import pytest

from pycaprio.mappings import AnnotationState
from pycaprio.core.adapters.http_adapter import HttpInceptionAdapter
from pycaprio.core.exceptions import IllegalIdentifier, InceptionBadResponse
from pycaprio.core.objects import Project, Document, Annotation, Curation


def mock_client(adapter: HttpInceptionAdapter) -> Mock:
    """The adapter's client is a Mock in these tests; expose it as such for the type checker."""
    return cast(Mock, adapter.client)


# A stream carrying a resolvable name, since document uploads require a file name and otherwise raise.
# The client is mocked in these tests, so the content is never read.
named_content = io.StringIO("")
named_content.name = "test-document.txt"

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
    assert getattr(mock_client(mock_http_adapter), verb).call_args[0][0] == route


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
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    mock_http_adapter.import_project(mock_io)
    assert mock_client(mock_http_adapter).post.call_args[0][0] == "/projects/import"


def test_import_project_returns_project(
    mock_http_adapter: HttpInceptionAdapter, mock_io: IO, mock_http_response: Mock, serialized_project: dict
):
    mock_http_response.json.return_value = {"body": serialized_project}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
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
    function: Callable[..., object],
    params: tuple,
    resource: dict,
    mock_http_adapter: HttpInceptionAdapter,
    mock_http_response: Mock,
    serializations: dict,
):
    mock_http_response.json.return_value = {"body": serializations[resource]}
    mock_client(mock_http_adapter).get.return_value = mock_http_response
    function(mock_http_adapter, *params)
    assert mock_client(mock_http_adapter).get.call_args[0][0] == route


def test_get_project_returns_good_instance(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_project: dict
):
    mock_http_response.json.return_value = {"body": serialized_project}
    mock_client(mock_http_adapter).get.return_value = mock_http_response
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
    mock_client(mock_http_adapter).get.return_value = mock_http_response
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
                named_content,
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
                named_content,
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
    function: Callable[..., object],
    params: tuple,
    resource: str,
    mock_http_adapter: HttpInceptionAdapter,
    mock_http_response: Mock,
    serializations: dict,
):
    mock_http_response.json.return_value = {"body": serializations[resource]}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    function(mock_http_adapter, *params)
    assert mock_client(mock_http_adapter).post.call_args[0][0] == route


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
                named_content,
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
                named_content,
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
    function: Callable[..., object],
    params: tuple,
    resource: str,
    mock_http_adapter: HttpInceptionAdapter,
    mock_http_response: Mock,
    serializations: dict,
    deserializations: dict,
):
    mock_http_response.json.return_value = {"body": serializations[resource]}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    response = function(mock_http_adapter, *params)
    assert isinstance(response, deserializations[resource].__class__)


def test_document_has_project_id_injected_document_list(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_document: dict
):
    test_project_id = 1
    mock_http_response.json.return_value = {"body": [serialized_document]}
    mock_client(mock_http_adapter).get.return_value = mock_http_response
    response = mock_http_adapter.documents(test_project_id)
    assert response[0].project_id == test_project_id


def test_document_has_project_id_injected_creation(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_document: dict
):
    test_project_id = 1
    mock_http_response.json.return_value = {"body": serialized_document}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    response = mock_http_adapter.create_document(test_project_id, "test-name", named_content)
    assert response.project_id == test_project_id


def test_annotation_has_project_id_injected_annotation_list(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_annotation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": [serialized_annotation]}
    mock_client(mock_http_adapter).get.return_value = mock_http_response
    response = mock_http_adapter.annotations(test_project_id, test_document_id)
    assert response[0].project_id == test_project_id


def test_annotation_has_document_id_injected_annotation_list(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_annotation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": [serialized_annotation]}
    mock_client(mock_http_adapter).get.return_value = mock_http_response
    response = mock_http_adapter.annotations(test_project_id, test_document_id)
    assert response[0].document_id == test_document_id


def test_annotation_has_project_id_injected_creation(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_annotation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": serialized_annotation}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    response = mock_http_adapter.create_annotation(test_project_id, test_document_id, "test-name", cast(IO, None))
    assert response.project_id == test_project_id


def test_annotation_has_document_id_injected_creation(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_annotation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": serialized_annotation}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    response = mock_http_adapter.create_annotation(test_project_id, test_document_id, "test-name", cast(IO, None))
    assert response.document_id == test_document_id


def test_curation_has_project_id_injected_creation(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_curation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": serialized_curation}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    response = mock_http_adapter.create_curation(test_project_id, test_document_id, cast(IO, None), "test-format")
    assert response.project_id == test_project_id


def test_curation_has_document_id_injected_creation(
    mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock, serialized_curation: dict
):
    test_project_id = 1
    test_document_id = 2
    mock_http_response.json.return_value = {"body": serialized_curation}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    response = mock_http_adapter.create_curation(test_project_id, test_document_id, cast(IO, None), "test-format")
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
):
    # The client's _request unpacks every files value as a (name, stream) tuple, so all content
    # uploads must pass files={"content": (name, stream)} rather than a bare stream. A named stream
    # is used so the document upload can resolve a file name (annotations/curations ignore it).
    mock_http_response.json.return_value = {"body": serializations[resource]}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    named_stream = io.StringIO("test-content")
    named_stream.name = "/tmp/example.txt"
    function(mock_http_adapter, *params, named_stream)
    content = mock_client(mock_http_adapter).post.call_args.kwargs["files"]["content"]
    _, stream = content
    assert stream is named_stream


def test_document_upload_uses_explicit_filename(mock_http_adapter, mock_http_response, serializations, mock_io):
    # An explicit filename is recorded as the uploaded file's name.
    mock_http_response.json.return_value = {"body": serializations["document"]}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    mock_http_adapter.create_document(1, "test-name", mock_io, filename="example.xmi")
    name, _ = mock_client(mock_http_adapter).post.call_args.kwargs["files"]["content"]
    assert name == "example.xmi"


def test_document_upload_derives_filename_from_file_object(mock_http_adapter, mock_http_response, serializations):
    # A real, named file object contributes its basename (path stripped) when no filename is given.
    mock_http_response.json.return_value = {"body": serializations["document"]}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    named_stream = io.StringIO("test-content")
    named_stream.name = "/tmp/example.xmi"
    mock_http_adapter.create_document(1, "test-name", named_stream)
    name, _ = mock_client(mock_http_adapter).post.call_args.kwargs["files"]["content"]
    assert name == "example.xmi"


def test_document_upload_derives_filename_from_bytes_path_file_object(
    mock_http_adapter, mock_http_response, serializations
):
    # A file opened with a bytes path has a bytes .name; its basename is still derived (decoded to str).
    mock_http_response.json.return_value = {"body": serializations["document"]}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    named_stream = io.StringIO("test-content")
    named_stream.name = b"/tmp/example.xmi"
    mock_http_adapter.create_document(1, "test-name", named_stream)
    name, _ = mock_client(mock_http_adapter).post.call_args.kwargs["files"]["content"]
    assert name == "example.xmi"


def test_document_upload_requires_resolvable_filename(mock_http_adapter, mock_http_response, serializations, mock_io):
    # An anonymous stream (no .name) with no explicit filename must raise rather than upload as "data".
    mock_http_response.json.return_value = {"body": serializations["document"]}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    with pytest.raises(ValueError):
        mock_http_adapter.create_document(1, "test-name", mock_io)


@pytest.mark.parametrize(
    "function, params, resource",
    [
        (HttpInceptionAdapter.create_annotation, (1, 1, "test-user"), "annotation"),
        (HttpInceptionAdapter.create_curation, (1, 1), "curation"),
    ],
)
def test_annotation_and_curation_upload_always_use_data_filename(
    function, params, resource, mock_http_adapter, mock_http_response, serializations
):
    # The server ignores the uploaded part name for annotations/curations, so it is always "data"
    # even when the content is a named file object.
    mock_http_response.json.return_value = {"body": serializations[resource]}
    mock_client(mock_http_adapter).post.return_value = mock_http_response
    named_stream = io.StringIO("test-content")
    named_stream.name = "/tmp/example.xmi"
    function(mock_http_adapter, *params, named_stream)
    name, _ = mock_client(mock_http_adapter).post.call_args.kwargs["files"]["content"]
    assert name == "data"


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


def error_response(message: str) -> Mock:
    """Builds the HTTP 500 error envelope INCEpTION returns, wrapping the given message."""
    response = Mock()
    response.status_code = 500
    response.text = f'{{"messages":[{{"level":"ERROR","message":"{message}"}}]}}'
    return response


def number_format_response(rejected_value: str, legacy: bool = False, parameter: str = "projectId") -> Mock:
    """
    Builds the HTTP 500 INCEpTION returns when it cannot parse a path variable as a long.

    The wording differs across versions, so both are exercised: 'legacy' is the message reported in
    issue #15 (with a nested NumberFormatException and no parameter name), the default is what
    current INCEpTION returns.
    """
    if legacy:
        message = (
            "Internal server error: Failed to convert value of type 'java.lang.String' to required "
            f"type 'long'; nested exception is java.lang.NumberFormatException: For input string: \\\"{rejected_value}\\\""
        )
    else:
        message = (
            f"Internal server error: Method parameter '{parameter}': Failed to convert value of type "
            f"'java.lang.String' to required type 'long'; For input string: \\\"{rejected_value}\\\""
        )
    return error_response(message)


# One representative per (verb, has-document-slot) combination the translation has to cover.
@pytest.mark.parametrize(
    "function, params",
    [
        (HttpInceptionAdapter.project, ("project-name",)),
        (HttpInceptionAdapter.delete_project, ("project-name",)),
        (HttpInceptionAdapter.assign_roles, ("project-name", "test-user", ["ANNOTATOR"])),
        (HttpInceptionAdapter.document, ("project-name", 1)),
        (HttpInceptionAdapter.delete_document, ("project-name", 1)),
        (HttpInceptionAdapter.update_annotation_state, ("project-name", 1, "test-user", AnnotationState.IN_PROGRESS)),
    ],
)
# Both INCEpTION wordings must be recognised: the current one and the older nested
# NumberFormatException reported in issue #15.
@pytest.mark.parametrize("legacy", [False, True])
def test_project_name_raises_illegal_identifier(function, params, legacy, mock_http_adapter):
    # Passing a project name where the remote API wants a numeric id must surface as an actionable
    # pycaprio error rather than INCEpTION's raw Java NumberFormatException.
    bad_response = number_format_response("project-name", legacy=legacy)
    for verb in ("get", "post", "delete"):
        getattr(mock_client(mock_http_adapter), verb).side_effect = InceptionBadResponse(bad_response)

    with pytest.raises(IllegalIdentifier) as exception_info:
        function(mock_http_adapter, *params)

    error = exception_info.value
    assert error.parameter_name == "project"
    assert error.identifier == "project-name"
    assert "project-name" in str(error)
    assert "numeric project ids" in str(error)
    assert "client.api.projects()" in str(error)
    # Stays catchable as the generic error, so existing handlers keep working.
    assert isinstance(error, InceptionBadResponse)


def test_document_name_raises_illegal_identifier(mock_http_adapter):
    # The same translation applies to document identifiers, attributed to the right parameter.
    bad_response = number_format_response("document-name")
    mock_client(mock_http_adapter).get.side_effect = InceptionBadResponse(bad_response)

    with pytest.raises(IllegalIdentifier) as exception_info:
        mock_http_adapter.document(1, "document-name")

    assert exception_info.value.parameter_name == "document"
    assert exception_info.value.identifier == "document-name"


def test_unrelated_number_format_error_is_not_translated(mock_http_adapter):
    # A NumberFormatException about a value we did not send is INCEpTION's own problem; it must
    # propagate untouched rather than being mislabelled as a bad project identifier.
    bad_response = number_format_response("something-internal")
    mock_client(mock_http_adapter).get.side_effect = InceptionBadResponse(bad_response)

    with pytest.raises(InceptionBadResponse) as exception_info:
        mock_http_adapter.documents(1)

    assert not isinstance(exception_info.value, IllegalIdentifier)


def test_out_of_range_numeric_id_is_not_translated(mock_http_adapter):
    # A numeric id too large for a Java long fails to parse for a completely different reason.
    # Claiming "ids must be numeric, not names or slugs" about it would be actively misleading.
    huge_id = "999999999999999999999999"
    bad_response = number_format_response(huge_id)
    mock_client(mock_http_adapter).get.side_effect = InceptionBadResponse(bad_response)

    with pytest.raises(InceptionBadResponse) as exception_info:
        mock_http_adapter.documents(huge_id)

    assert not isinstance(exception_info.value, IllegalIdentifier)


def test_attribution_follows_the_parameter_the_server_reports(mock_http_adapter):
    # When both identifiers are the same string, matching on the value alone cannot tell them apart.
    # INCEpTION says which path variable it was binding, so that must win over the document-first
    # guess -- otherwise the error points at the wrong argument and hints at a lookup call
    # (client.api.documents(project)) that needs the very project that is broken.
    bad_response = number_format_response("bad", parameter="projectId")
    mock_client(mock_http_adapter).get.side_effect = InceptionBadResponse(bad_response)

    with pytest.raises(IllegalIdentifier) as exception_info:
        mock_http_adapter.document("bad", "bad")

    assert exception_info.value.parameter_name == "project"
    assert "client.api.projects()" in str(exception_info.value)


def test_attribution_follows_reported_document_parameter(mock_http_adapter):
    # The same deference applies when the server blames the document id.
    bad_response = number_format_response("bad", parameter="documentId")
    mock_client(mock_http_adapter).get.side_effect = InceptionBadResponse(bad_response)

    with pytest.raises(IllegalIdentifier) as exception_info:
        mock_http_adapter.document("bad", "bad")

    assert exception_info.value.parameter_name == "document"


def test_ambiguous_identifiers_without_reported_parameter_blame_the_document(mock_http_adapter):
    # Older INCEpTION reports no parameter name, so the document-first fallback still applies.
    bad_response = number_format_response("bad", legacy=True)
    mock_client(mock_http_adapter).get.side_effect = InceptionBadResponse(bad_response)

    with pytest.raises(IllegalIdentifier) as exception_info:
        mock_http_adapter.document("bad", "bad")

    assert exception_info.value.parameter_name == "document"


def test_conversion_failure_is_not_spliced_across_messages(mock_http_adapter):
    # The error body is a JSON array of messages. A "Failed to convert" in one entry must not be
    # stitched onto a "For input string" from an unrelated entry, which would pin a valid numeric
    # id as illegal.
    response = Mock()
    response.status_code = 500
    # Note the single-backslash escaping: this is what a real JSON error body contains, and what
    # number_format_response() produces for the single-message case.
    response.text = (
        '{"messages":['
        '{"level":"ERROR","message":"Failed to convert value of type Foo to required type \'long\'"},'
        '{"level":"WARN","message":"unrelated batch failure: For input string: \\"77\\""}'
        "]}"
    )
    mock_client(mock_http_adapter).get.side_effect = InceptionBadResponse(response)

    with pytest.raises(InceptionBadResponse) as exception_info:
        mock_http_adapter.documents(77)

    assert not isinstance(exception_info.value, IllegalIdentifier)


def test_unrelated_server_error_is_not_translated(mock_http_adapter):
    # An ordinary failure must keep its original error.
    bad_response = error_response("Internal server error: something else")
    mock_client(mock_http_adapter).get.side_effect = InceptionBadResponse(bad_response)

    with pytest.raises(InceptionBadResponse) as exception_info:
        mock_http_adapter.documents("project-name")

    assert not isinstance(exception_info.value, IllegalIdentifier)


def test_numeric_string_project_id_still_works(mock_http_adapter, mock_http_response, serializations):
    # A numeric id passed as a string is legitimate and must not be affected by the translation.
    mock_http_response.json.return_value = {"body": [serializations["document"]]}
    mock_client(mock_http_adapter).get.return_value = mock_http_response
    mock_http_adapter.documents("1")
    assert mock_client(mock_http_adapter).get.call_args.args[0] == "/projects/1/documents"


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
    assert getattr(mock_client(mock_http_adapter), verb).call_args[0][0] == route


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
    mock_client(mock_http_adapter).get.return_value = mock_http_response
    assert mock_http_adapter.list_roles(1, "test-user") == ["MANAGER", "CURATOR"]


def test_role_methods_tolerate_empty_response_body(mock_http_adapter: HttpInceptionAdapter, mock_http_response: Mock):
    # A mutating permission endpoint may answer with no content; that must yield [] rather than
    # a JSONDecodeError from response.json() on an empty body.
    mock_http_response.content = b""
    mock_http_response.json.side_effect = ValueError("No JSON object could be decoded")
    mock_client(mock_http_adapter).delete.return_value = mock_http_response
    assert mock_http_adapter.delete_roles(1, "test-user", ["MANAGER"]) == []


def test_assign_roles_passes_roles_as_query_params(mock_http_adapter: HttpInceptionAdapter):
    # The API reads 'roles' as a query parameter, so it must be sent via params, not the form body.
    mock_http_adapter.assign_roles(1, "test-user", ["MANAGER", "CURATOR"])
    call = mock_client(mock_http_adapter).post.call_args
    assert call.kwargs.get("params") == {"roles": ["MANAGER", "CURATOR"]}
    assert call.kwargs.get("data") is None


def test_delete_roles_passes_roles_as_query_params(mock_http_adapter: HttpInceptionAdapter):
    mock_http_adapter.delete_roles(1, "test-user", ["MANAGER"])
    assert mock_client(mock_http_adapter).delete.call_args.kwargs.get("params") == {"roles": ["MANAGER"]}


def test_role_methods_url_encode_user_id(mock_http_adapter: HttpInceptionAdapter):
    mock_http_adapter.list_roles(1, "user/with space")
    assert mock_client(mock_http_adapter).get.call_args[0][0] == "/projects/1/permissions/user%2Fwith%20space"


def test_annotation_methods_url_encode_user_name(mock_http_adapter: HttpInceptionAdapter):
    encoded = "user%2Fwith%20space"

    mock_http_adapter.annotation(1, 1, "user/with space")
    assert mock_client(mock_http_adapter).get.call_args[0][0] == f"/projects/1/documents/1/annotations/{encoded}"

    mock_http_adapter.delete_annotation(1, 1, "user/with space")
    assert mock_client(mock_http_adapter).delete.call_args[0][0] == f"/projects/1/documents/1/annotations/{encoded}"

    mock_http_adapter.update_annotation_state(1, 1, "user/with space", "NEW")
    assert mock_client(mock_http_adapter).post.call_args[0][0] == f"/projects/1/documents/1/annotations/{encoded}/state"


def test_assign_roles_empty_list_raises(mock_http_adapter: HttpInceptionAdapter):
    # An empty list would be dropped from the query string, so reject it client-side.
    with pytest.raises(ValueError):
        mock_http_adapter.assign_roles(1, "test-user", [])
    mock_client(mock_http_adapter).post.assert_not_called()


def test_delete_roles_empty_list_raises(mock_http_adapter: HttpInceptionAdapter):
    with pytest.raises(ValueError):
        mock_http_adapter.delete_roles(1, "test-user", [])
    mock_client(mock_http_adapter).delete.assert_not_called()
