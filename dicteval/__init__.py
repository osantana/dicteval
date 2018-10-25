import copy
import functools
import json
import operator
import re

from .exceptions import FunctionNotFound


class LanguageSpecification:
    def __getitem__(self, item):
        if not item:
            item = "nop"
        if item.startswith('lambda'):
            item = "lambda"
        try:
            return getattr(self, f"function_{item}")
        except AttributeError:
            raise FunctionNotFound(f"Function {item} not found.")


class Function:
    def __init__(self, arg_names, body, evaluator, context):
        self.arg_names = arg_names
        self.body = body
        self.evaluator = evaluator
        self.context = context

    def __call__(self, *args):
        local_context = copy.deepcopy(self.context)
        local_context.update(zip(self.arg_names, args))
        return self.evaluator(self.body, local_context)


class BuiltinLanguage(LanguageSpecification):
    def function_lambda(self, value, evaluator, context, args):
        return Function(args, value, evaluator, context)

    def function_filter(self, value, evaluator, context):
        filter_function = evaluator(value[0], context)
        return list(filter(filter_function, (evaluator(v, context) for v in value[1])))

    def function_map(self, value, evaluator, context):
        map_function = evaluator(value[0], context)
        return list(map(map_function, (evaluator(v, context) for v in value[1])))

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
        return sum(evaluator(value, context))

    def function_mul(self, value, evaluator, context):
        return functools.reduce(operator.mul, (evaluator(v, context) for v in value))

    def function_pow(self, value, evaluator, context):
        return functools.reduce(lambda x, y: x ** y, (evaluator(v, context) for v in value))

    def function_divmod(self, value, evaluator, context):
        return divmod(*evaluator(value, context))

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

            func_name = key[1:]
            func = self.language[func_name]

            if func_name.startswith("lambda"):
                args = self._extract_args(func_name)
                return func(value, self, context, args)

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

    def _extract_args(self, lambda_definition):
        arg_names = [arg.strip() for arg in lambda_definition.replace("lambda", "").strip("()").split(",") if arg]
        for arg_name in arg_names:
            if not arg_name[0].isalpha():
                raise TypeError("Invalid lambda argument name {!r}".format(arg_name))
        return arg_names


dicteval = Evaluator(BuiltinLanguage)


def jsoneval(string):
    return dicteval(json.loads(string))
