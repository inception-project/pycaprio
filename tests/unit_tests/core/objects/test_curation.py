import pytest


def test_str_ok(deserialized_curation):
    try:
        str(deserialized_curation)
    except:
        pytest.fail()


def test_repr_ok(deserialized_curation):
    try:
        repr(deserialized_curation)
    except:
        pytest.fail()
