from pycaprio.core.objects.curation import Curation
from pycaprio.core.schemas.curation import CurationSchema


def test_curation_schema_dump_one_dict_many_false(curation_schema: CurationSchema,
                                                  deserialized_curation: Curation,
                                                  serialized_curation: dict):
    assert curation_schema.dump(deserialized_curation) == serialized_curation


def test_curation_schema_dump_one_dict_many_true(curation_schema: CurationSchema,
                                                 deserialized_curation: Curation,
                                                 serialized_curation: dict):
    assert curation_schema.dump([deserialized_curation], many=True) == [serialized_curation]


def test_curation_schema_dump_list_many_true(curation_schema: CurationSchema,
                                             deserialized_curation: Curation):
    assert type(curation_schema.dump([deserialized_curation], many=True)) is list


def test_curation_schema_dump_list_no_empty_many_true(curation_schema: CurationSchema,
                                                      deserialized_curation: Curation):
    assert len(curation_schema.dump([deserialized_curation], many=True)) == 1


def test_curation_schema_dump_list_of_dicts_many_true(curation_schema: CurationSchema,
                                                      deserialized_curation: Curation):
    assert type(curation_schema.dump([deserialized_curation], many=True)[0]) is dict


def test_curation_schema_load_one_dict_many_false(curation_schema: CurationSchema,
                                                  deserialized_curation: Curation,
                                                  serialized_curation: dict):
    assert curation_schema.load(serialized_curation) == deserialized_curation


def test_curation_schema_load_one_dict_many_true(curation_schema: CurationSchema,
                                                 deserialized_curation: Curation,
                                                 serialized_curation: dict):
    assert curation_schema.load([serialized_curation], many=True) == [deserialized_curation]


def test_curation_schema_load_list_many_true(curation_schema: CurationSchema, serialized_curation: dict):
    assert type(curation_schema.load([serialized_curation], many=True)) is list


def test_curation_schema_load_list_no_empty_many_true(curation_schema: CurationSchema,
                                                      serialized_curation: dict):
    assert len(curation_schema.load([serialized_curation], many=True)) == 1


def test_curation_schema_load_list_of_dicts_many_true(curation_schema: CurationSchema,
                                                      serialized_curation: dict):
    assert type(curation_schema.load([serialized_curation], many=True)[0]) is Curation
