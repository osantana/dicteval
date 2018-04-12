import pytest

from dicteval import dicteval, jsoneval, BuiltinLanguage


@pytest.mark.parametrize("expression,result", [
    (3, 3),
    ([3], [3]),
    ([3, 5], [3, 5]),
    ((3, 5), [3, 5]),
    ("x", "x"),
    ({"=": 3}, 3),
    ({"=": [3, 5]}, [3, 5]),
    ({"=": 3, "ignore": 5}, 3),
    ({"=sum": [3, 5]}, 8),
    ({"=sum": (3, 5)}, 8),
    ({"=sum": {"=": [3, 5]}}, 8)
])
def test_basic_eval(expression, result):
    assert dicteval(expression) == result


def test_context_eval(context):
    assert dicteval('''@{varobj.attr + " = 'object.attr'"}''', context) == "object.attr = 'object.attr'"


def test_invalid_expression_object_with_no_result_key():
    with pytest.raises(ValueError):
        dicteval({"no_result_error": 0})


def test_json_loads():
    assert jsoneval('{"=": 3}') == 3


def test_buitin_language(context):
    language = BuiltinLanguage()
    assert language["sum"]([1, 2], dicteval, context) == 3
