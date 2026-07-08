import pytest

from pycaprio.core.mappings import RoleType


def test_list_roles(pycaprio, test_name, test_user):
    project = pycaprio.api.create_project(test_name)
    roles = pycaprio.api.list_roles(project, test_user)
    assert roles, "the project creator should have at least one role"
    assert all(isinstance(role, str) for role in roles)
    # The project creator is automatically granted the manager role.
    assert RoleType.MANAGER in roles


def test_assign_roles(pycaprio, test_name, test_user):
    project = pycaprio.api.create_project(test_name)
    # Establish a known starting state (role absent) rather than relying on default roles.
    pycaprio.api.delete_roles(project, test_user, [RoleType.CURATOR])
    assert RoleType.CURATOR not in pycaprio.api.list_roles(project, test_user)
    returned_roles = pycaprio.api.assign_roles(project, test_user, [RoleType.CURATOR])
    assert RoleType.CURATOR in returned_roles
    assert RoleType.CURATOR in pycaprio.api.list_roles(project, test_user)


def test_delete_roles(pycaprio, test_name, test_user):
    project = pycaprio.api.create_project(test_name)
    # Ensure the role is present first so the test does not depend on default roles.
    pycaprio.api.assign_roles(project, test_user, [RoleType.CURATOR])
    assert RoleType.CURATOR in pycaprio.api.list_roles(project, test_user)
    returned_roles = pycaprio.api.delete_roles(project, test_user, [RoleType.CURATOR])
    assert RoleType.CURATOR not in returned_roles
    assert RoleType.CURATOR not in pycaprio.api.list_roles(project, test_user)


def test_role_methods_reject_empty_list(pycaprio, test_name, test_user):
    # An empty list is dropped from the query string, so the client rejects it up front rather
    # than issuing a request the server cannot satisfy.
    project = pycaprio.api.create_project(test_name)
    with pytest.raises(ValueError):
        pycaprio.api.assign_roles(project, test_user, [])
    with pytest.raises(ValueError):
        pycaprio.api.delete_roles(project, test_user, [])
