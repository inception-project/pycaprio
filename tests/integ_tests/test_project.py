import pytest

from pycaprio.core.exceptions import IllegalIdentifier
from pycaprio.core.objects import Project


def test_list_projects(pycaprio, test_name):
    pycaprio.api.create_project(test_name)
    projects = pycaprio.api.projects()
    assert projects
    assert all(isinstance(project, Project) for project in projects)


def test_create_project(pycaprio, test_name):
    initial_projects = list(pycaprio.api.projects())
    project = pycaprio.api.create_project(test_name)
    assert isinstance(project, Project)
    assert project not in initial_projects
    assert project in list(pycaprio.api.projects())


def test_delete_project(pycaprio, test_name):
    project = pycaprio.api.create_project(test_name)
    pycaprio.api.delete_project(project)
    assert project not in pycaprio.api.projects()


def test_detail_project(pycaprio, test_name):
    project = pycaprio.api.create_project(test_name)
    assert project == pycaprio.api.project(project)


def test_project_by_name_against_live_inception(pycaprio, test_name):
    """
    Pins the behaviour of looking a project up by name (its URL slug) rather than by numeric id
    against a real INCEpTION.

    Two outcomes are acceptable, and which one occurs tells us where upstream stands:

    - The remote API rejects the name while parsing it as a numeric id. pycaprio must translate that
      into an IllegalIdentifier instead of leaking a Java NumberFormatException.
    - The remote API resolves the name, meaning inception-project/inception#3457 has landed. The
      translation is then simply never triggered and the lookup returns the right project.

    If this starts taking the second branch, the translation code in HttpInceptionAdapter has become
    dead weight and can be retired.
    """
    project = pycaprio.api.create_project(test_name)

    try:
        resolved = pycaprio.api.project(project.project_name)
    except IllegalIdentifier as error:
        # Current behaviour: names are not supported, but the error is now actionable.
        assert project.project_name in str(error)
        assert error.parameter_name == "project"
        pytest.skip(
            "This INCEpTION does not support project names/slugs in the remote API "
            "(inception-project/inception#3457); pycaprio reported it clearly."
        )

    # Future behaviour: upstream resolves slugs, so the lookup must return the same project.
    assert resolved == project
