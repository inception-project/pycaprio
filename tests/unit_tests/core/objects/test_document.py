import pytest


def test_str_ok(deserialized_document):
    try:
        str(deserialized_document)
    except:
        pytest.fail()


def test_repr_ok(deserialized_document):
    try:
        repr(deserialized_document)
    except:
        pytest.fail()
