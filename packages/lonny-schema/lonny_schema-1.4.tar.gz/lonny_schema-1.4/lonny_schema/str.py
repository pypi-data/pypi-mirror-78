from .type import TypeValidator
from .len import LengthValidator
from .base import Validator

class StrValidator(Validator):
    def __init__(self, *, min_length = None, max_length = None):
        self._min_length = min_length
        self._max_length = max_length

    def validate(self, ctx, value):
        TypeValidator(str).validate(ctx, value)
        LengthValidator(min_length=self._min_length, max_length=self._max_length).validate(ctx, value)