from pycaprio.core.objects.project import Project
from pycaprio.core.schemas.project import ProjectSchema


def test_project_schema_dump_one_dict_many_false(
    project_schema: ProjectSchema, deserialized_project: Project, serialized_project: dict
):
    assert project_schema.dump(deserialized_project) == serialized_project


def test_project_schema_dump_one_dict_many_true(
    project_schema: ProjectSchema, deserialized_project: Project, serialized_project: dict
):
    assert project_schema.dump([deserialized_project], many=True) == [serialized_project]


def test_project_schema_dump_list_many_true(project_schema: ProjectSchema, deserialized_project: Project):
    assert type(project_schema.dump([deserialized_project], many=True)) is list


def test_project_schema_dump_list_no_empty_many_true(project_schema: ProjectSchema, deserialized_project: Project):
    assert len(project_schema.dump([deserialized_project], many=True)) == 1


def test_project_schema_dump_list_of_dicts_many_true(project_schema: ProjectSchema, deserialized_project: Project):
    assert type(project_schema.dump([deserialized_project], many=True)[0]) is dict


def test_project_schema_load_one_dict_many_false(
    project_schema: ProjectSchema, deserialized_project: Project, serialized_project: dict
):
    assert project_schema.load(serialized_project) == deserialized_project


def test_project_schema_load_one_dict_many_true(
    project_schema: ProjectSchema, deserialized_project: Project, serialized_project: dict
):
    assert project_schema.load([serialized_project], many=True) == [deserialized_project]


def test_project_schema_load_list_many_true(project_schema: ProjectSchema, serialized_project: dict):
    assert type(project_schema.load([serialized_project], many=True)) is list


def test_project_schema_load_list_no_empty_many_true(project_schema: ProjectSchema, serialized_project: dict):
    assert len(project_schema.load([serialized_project], many=True)) == 1


def test_project_schema_load_list_of_dicts_many_true(project_schema: ProjectSchema, serialized_project: dict):
    assert type(project_schema.load([serialized_project], many=True)[0]) is Project
