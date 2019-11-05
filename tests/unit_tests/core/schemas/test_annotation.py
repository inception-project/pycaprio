from pycaprio.core.objects.annotation import Annotation
from pycaprio.core.schemas.annotation import AnnotationSchema


def test_annotation_schema_dump_one_dict_many_false(annotation_schema: AnnotationSchema,
                                                    deserialized_annotation: Annotation,
                                                    serialized_annotation: dict):
    assert annotation_schema.dump(deserialized_annotation) == serialized_annotation


def test_annotation_schema_dump_one_dict_many_true(annotation_schema: AnnotationSchema,
                                                   deserialized_annotation: Annotation,
                                                   serialized_annotation: dict):
    assert annotation_schema.dump([deserialized_annotation], many=True) == [serialized_annotation]


def test_annotation_schema_dump_list_many_true(annotation_schema: AnnotationSchema,
                                               deserialized_annotation: Annotation):
    assert type(annotation_schema.dump([deserialized_annotation], many=True)) is list


def test_annotation_schema_dump_list_no_empty_many_true(annotation_schema: AnnotationSchema,
                                                        deserialized_annotation: Annotation):
    assert len(annotation_schema.dump([deserialized_annotation], many=True)) == 1


def test_annotation_schema_dump_list_of_dicts_many_true(annotation_schema: AnnotationSchema,
                                                        deserialized_annotation: Annotation):
    assert type(annotation_schema.dump([deserialized_annotation], many=True)[0]) is dict


def test_annotation_schema_load_one_dict_many_false(annotation_schema: AnnotationSchema,
                                                    deserialized_annotation: Annotation,
                                                    serialized_annotation: dict):
    assert annotation_schema.load(serialized_annotation) == deserialized_annotation


def test_annotation_schema_load_one_dict_many_true(annotation_schema: AnnotationSchema,
                                                   deserialized_annotation: Annotation,
                                                   serialized_annotation: dict):
    assert annotation_schema.load([serialized_annotation], many=True) == [deserialized_annotation]


def test_annotation_schema_load_list_many_true(annotation_schema: AnnotationSchema, serialized_annotation: dict):
    assert type(annotation_schema.load([serialized_annotation], many=True)) is list


def test_annotation_schema_load_list_no_empty_many_true(annotation_schema: AnnotationSchema,
                                                        serialized_annotation: dict):
    assert len(annotation_schema.load([serialized_annotation], many=True)) == 1


def test_annotation_schema_load_list_of_dicts_many_true(annotation_schema: AnnotationSchema,
                                                        serialized_annotation: dict):
    assert type(annotation_schema.load([serialized_annotation], many=True)[0]) is Annotation


def test_annotation_schema_load_null_datetime_as_none(annotation_schema: AnnotationSchema,
                                                      serialized_annotation: dict):
    serialized_annotation['timestamp'] = None
    annotation = annotation_schema.load(serialized_annotation)
    assert annotation.timestamp is None


def test_annotation_schema_dump_none_datetime_as_null(annotation_schema: AnnotationSchema,
                                                      deserialized_annotation: Annotation):
    deserialized_annotation.timestamp = None
    assert annotation_schema.dump(deserialized_annotation)['timestamp'] is None
