import pytest


def test_str_ok(deserialized_project):
    try:
        str(deserialized_project)
    except:
        pytest.fail()


def test_repr_ok(deserialized_project):
    try:
        repr(deserialized_project)
    except:
        pytest.fail()
