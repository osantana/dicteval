import pytest

from dicteval import BuiltinLanguage, dicteval, jsoneval
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
    ({"=sum": {"=": [3, 5]}}, 8),
    ({"=mul": (5, 3, 2, -1)}, -30),
    ({"=map(lambda x: x**2)": [5, 6, -7]},[25,36,49]),
    ({"=filter(lambda x: x>20)": [10, 18, 22,3,-10,50,800]},[22,50,800]),
    ({"=all": (True, True, True)}, True),
    ({"=all": {"=": (True, True, True)}}, True),
    ({"=all": (True, False, True)}, False),
    ({"=all": (False, False, False)}, False),
    ({"=divmod": (8, 3)}, (2, 2)),
    ({"=divmod": [8, 3]}, (2, 2)),
    ({"=divmod": {"=": [8, 3]}}, (2, 2)),
    ({"=divmod": (7.5, 2.5)}, (3.0, 0.0)),
    ({"=zip": ([1, 2, 3], [4, 5], {"=": [6, 7, 8, 9]})}, [(1, 4, 6), (2, 5, 7)]),
])
def test_basic_eval(expression, result):
    assert dicteval(expression) == result


def test_context_eval(context):
    assert dicteval('''@{varobj.attr + " = 'object.attr'"}''', context) == "object.attr = 'object.attr'"


def test_invalid_expression_object_with_no_result_key():
    with pytest.raises(ValueError):
        dicteval({"no_result_error": 0})


def test_json_loads():
    assert jsoneval('{"=": [true, false, null]}') == [True, False, None]


@pytest.mark.parametrize("fn,args,result", [
    ("any", (1, 2, 3), True),
    ("any", (0, 0), False),
    ("eq", (1, 1, 1, 1, 1), True),
    ("eq", (1, 1, 5, 1, 1), False),
    ("neq", (1, 1, 1, 1, 1), False),
    ("neq", (1, 1, 5, 1, 1), True),
    ("nop", 4, 4),
    ("not", True, False),
    ("not", False, True),
    ("sum", (1, 2), 3),
    ("mul", (2, 4), 8),
    ("all", tuple(), True),
    ("all", (True, True), True),
    ("all", (True, False), False),
    ("divmod", (8, 3), (2, 2)),
    ("divmod", (7.5, 2.5), (3.0, 0.0)),
])
def test_buitin_language(fn, args, result, context):
    language = BuiltinLanguage()
    assert language[fn](args, dicteval, context) == result


def test_function_not_found_error():
    language = BuiltinLanguage()
    with pytest.raises(FunctionNotFound):
        return language["not_found"]
