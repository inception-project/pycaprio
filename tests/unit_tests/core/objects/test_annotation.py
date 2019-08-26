import pytest


def test_str_ok(deserialized_annotation):
    try:
        str(deserialized_annotation)
    except:
        pytest.fail()


def test_repr_ok(deserialized_annotation):
    try:
        repr(deserialized_annotation)
    except:
        pytest.fail()
