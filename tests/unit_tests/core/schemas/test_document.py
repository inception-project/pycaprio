from pycaprio.core.objects.document import Document
from pycaprio.core.schemas.document import DocumentSchema


def test_document_schema_dump_one_dict_many_false(document_schema: DocumentSchema, deserialized_document: Document,
                                                  serialized_document: dict):
    assert document_schema.dump(deserialized_document) == serialized_document


def test_document_schema_dump_one_dict_many_true(document_schema: DocumentSchema, deserialized_document: Document,
                                                 serialized_document: dict):
    assert document_schema.dump([deserialized_document], many=True) == [serialized_document]


def test_document_schema_dump_list_many_true(document_schema: DocumentSchema, deserialized_document: Document):
    assert type(document_schema.dump([deserialized_document], many=True)) is list


def test_document_schema_dump_list_no_empty_many_true(document_schema: DocumentSchema, deserialized_document: Document):
    assert len(document_schema.dump([deserialized_document], many=True)) == 1


def test_document_schema_dump_list_of_dicts_many_true(document_schema: DocumentSchema, deserialized_document: Document):
    assert type(document_schema.dump([deserialized_document], many=True)[0]) is dict


def test_document_schema_load_one_dict_many_false(document_schema: DocumentSchema, deserialized_document: Document,
                                                  serialized_document: dict):
    assert document_schema.load(serialized_document) == deserialized_document


def test_document_schema_load_one_dict_many_true(document_schema: DocumentSchema, deserialized_document: Document,
                                                 serialized_document: dict):
    assert document_schema.load([serialized_document], many=True) == [deserialized_document]


def test_document_schema_load_list_many_true(document_schema: DocumentSchema, serialized_document: dict):
    assert type(document_schema.load([serialized_document], many=True)) is list


def test_document_schema_load_list_no_empty_many_true(document_schema: DocumentSchema, serialized_document: dict):
    assert len(document_schema.load([serialized_document], many=True)) == 1


def test_document_schema_load_list_of_dicts_many_true(document_schema: DocumentSchema, serialized_document: dict):
    assert type(document_schema.load([serialized_document], many=True)[0]) is Document
