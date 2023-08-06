from .base import Validator

class LengthValidator(Validator):
    def __init__(self, *, min_length = None, max_length = None):
        self._min_length = min_length
        self._max_length = max_length

    def validate(self, ctx, value):
        if self._min_length is not None and self._min_length > len(value):
            ctx.error("value is too short", length = len(value), min_length = self._min_length)
        if self._max_length is not None and self._max_length < len(value):
            ctx.error("value is too long", length = len(value), max_length = self._max_length)