from .type import TypeValidator
from .base import Validator
from .dummy import DummyValidator
from .len import LengthValidator

class ItemsValidator(Validator):
    def __init__(self, *, min_length = None, max_length = None, key_validator = DummyValidator(), value_validator = DummyValidator()):
        self._key_validator = key_validator
        self._value_validator = value_validator
        self._min_length = min_length
        self._max_length = max_length
    def validate(self, ctx, value):
        TypeValidator(dict).validate(ctx, value)
        LengthValidator(min_length=self._min_length, max_length=self._max_length).validate(ctx, value)
        for key, value in value.items():
            self._key_validator.validate(ctx[key]["$key"])
            self._value_validator.validate(ctx[key])