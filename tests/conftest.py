import pytest


@pytest.fixture
def context():
    class PlainObject:
        attr = "object.attr"

    return {"varint": 1, "varstr": "str", "varobj": PlainObject()}
