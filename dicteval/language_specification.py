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
