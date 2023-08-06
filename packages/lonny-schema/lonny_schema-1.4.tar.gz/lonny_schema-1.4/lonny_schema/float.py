from .type import TypeValidator
from .base import Validator

class FloatValidator(Validator):
    def __init__(self, *, min_value = None, max_value = None):
        self._min_value = min_value
        self._max_value = max_value

    def validate(self, ctx, value):
        TypeValidator(float).validate(ctx, value)
        if self._min_value is not None and self._min_value > value:
            ctx.error("value is too small", value = value, min_value = self._min_value)
        if self._max_value is not None and self._max_value < value:
            ctx.error("value is too large", value = value, max_value = self._max_value)