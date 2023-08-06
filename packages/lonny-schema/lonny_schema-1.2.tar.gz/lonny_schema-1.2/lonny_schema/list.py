from .type import TypeValidator
from .len import LengthValidator
from .dummy import DummyValidator
from .base import Validator

class ListValidator(Validator):
    def __init__(self, validator = DummyValidator(), *, min_length = None, max_length = None):
        self._validator = validator
        self._min_length = min_length
        self._max_length = max_length

    def validate(self, ctx, value):
        TypeValidator(list).validate(ctx, value)
        LengthValidator(min_length=self._min_length, max_length=self._max_length).validate(ctx, value)
        for ix, el in enumerate(value):
            self._validator.validate(ctx[ix], el)