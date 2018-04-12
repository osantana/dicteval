import pytest

from dicteval import dicteval, jsoneval, BuiltinLanguage
from dicteval.exceptions import FunctionNotFound


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
    assert jsoneval('{"=": [true, null]}') == [True, None]


@pytest.mark.parametrize("fn,args,result", [
    ("eq", (1, 1, 1, 1, 1), True),
    ("eq", (1, 1, 5, 1, 1), False),
    ("neq", (1, 1, 1, 1, 1), False),
    ("neq", (1, 1, 5, 1, 1), True),
    ("nop", 4, 4),
    ("not", True, False),
    ("not", False, True),
    ("sum", (1, 2), 3),
])
def test_buitin_language(fn, args, result, context):
    language = BuiltinLanguage()
    assert language[fn](args, dicteval, context) == result


def test_function_not_found_error():
    language = BuiltinLanguage()
    with pytest.raises(FunctionNotFound):
        return language["not_found"]
