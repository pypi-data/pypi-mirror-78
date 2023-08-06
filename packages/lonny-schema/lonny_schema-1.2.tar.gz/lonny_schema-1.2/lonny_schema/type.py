from .base import Validator

class TypeValidator(Validator):
    def __init__(self, type):
        self._type = type

    def validate(self, ctx, value):
        if not isinstance(value, self._type):
            ctx.error(f"the type is wrong", value = value, type = str(type(value)), expected_type = str(self._type))