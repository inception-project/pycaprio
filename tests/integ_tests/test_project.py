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
