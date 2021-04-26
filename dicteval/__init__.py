
import json
from .exceptions import FunctionNotFound
from .builtin_language import BuiltinLanguage
from .evaluator import Evaluator

dicteval = Evaluator(BuiltinLanguage)

def jsoneval(string):
    return dicteval(json.loads(string))
