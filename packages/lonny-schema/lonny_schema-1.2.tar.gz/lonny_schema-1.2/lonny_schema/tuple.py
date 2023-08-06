from .type import TypeValidator
from .base import Validator

class TupleValidator(Validator):
    def __init__(self, * validators):
        self._validators = validators

    def validate(self, ctx, value):
        TypeValidator(list).validate(ctx, value)
        num_validators = len(self._validators)
        if num_validators != len(value):
            ctx.error(f"Expected a {num_validators}-tuple", n = len(value))
        for ix, validator in enumerate(self._validators):
            validator.validate(ctx[ix], value[ix])