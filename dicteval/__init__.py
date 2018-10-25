import functools
import json
import operator
import re

from .exceptions import FunctionNotFound


class LanguageSpecification:
    def __getitem__(self, item):
        if not item:
            item = "nop"
        if item.startswith('map'):
            item = "map"
        if item.startswith('filter'):
            item = "filter"
        try:
            return getattr(self, f"function_{item}")
        except AttributeError:
            raise FunctionNotFound(f"Function {item} not found.")


class BuiltinLanguage(LanguageSpecification):
    def function_any(self, value, evaluator, context):
        return any(evaluator(v, context) for v in value)

    def function_all(self, value, evaluator, context):
        return all(evaluator(v, context) for v in value)

    def function_eq(self, value, evaluator, context):
        value = [evaluator(v, context) for v in value]
        return not value or value.count(value[0]) == len(value)

    def function_if(self, value, evaluator, context):
        values = [evaluator(v, context) for v in value]
        condition, t = values[0:2]
        f = values[2] if len(values) > 2 else None
        return t if condition else f

    def function_neq(self, value, evaluator, context):
        return not self.function_eq(value, evaluator, context)

    def function_nop(self, value, evaluator, context):
        return evaluator(value, context)

    def function_not(self, value, evaluator, context):
        return not evaluator(value, context)

    def function_sum(self, value, evaluator, context):
        return sum(evaluator(v, context) for v in value)

    def function_mul(self, value, evaluator, context):
        return functools.reduce(operator.mul, (evaluator(v, context) for v in value))

    def function_divmod(self, value, evaluator, context):
        return divmod(*evaluator(value, context))

    def function_map(self, func, value, evaluator, context):
        return [func(e) for e in [evaluator(v, context) for v in value]]

    def function_filter(self, func, value, evaluator, context):
        return list(filter(func, (evaluator(v, context) for v in value)))

    def function_zip(self, value, evaluator, context):
        lists = [evaluator(v, context) for v in value]
        return list(zip(*lists))


class Evaluator:
    def __init__(self, language_spec):
        self.language = language_spec()

    def __call__(self, expr, context=None):
        if context is None:
            context = {}

        if isinstance(expr, dict):
            expression_keys = [k for k in expr if k.startswith("=")]
            if len(expression_keys) != 1:
                raise ValueError("Invalid expression")

            key = expression_keys[0]
            value = expr[key]

            if isinstance(value, dict):
                value = self(value, context)

            func = self.language[key[1:]]

            if func.__name__ in ['function_map', 'function_filter']:
                coll_func = re.search(r'(map|filter)\((.*)\)', key).groups()[1]
                return func(eval(coll_func), value, self, context)

            return func(value, self, context)

        if isinstance(expr, (list, tuple)):
            return [self(v, context) for v in expr]

        # TODO: implement a safe eval here
        if isinstance(expr, str):
            if expr.startswith("@{") and expr.endswith("}"):
                return eval(expr[2:-1], {}, context)
            if expr.startswith("!{") and expr.endswith("}"):
                return context[expr[2:-1]]

        return expr


dicteval = Evaluator(BuiltinLanguage)


def jsoneval(string):
    return dicteval(json.loads(string))
