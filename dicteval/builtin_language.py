import operator
import functools
from .language_specification import LanguageSpecification

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
