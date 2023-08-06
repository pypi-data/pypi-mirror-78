from .base import Validator

class AllValidator(Validator):
    def __init__(self, *validators):
        self._validators = validators

    def validate(self, ctx, value):
        for val in self._validators:
            val.validate(ctx, value)