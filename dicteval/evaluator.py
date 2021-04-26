import re

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
