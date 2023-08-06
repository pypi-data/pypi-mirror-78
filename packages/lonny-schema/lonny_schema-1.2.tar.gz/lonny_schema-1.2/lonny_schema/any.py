from .error import ValidationError
from .base import Validator

class AnyValidator(Validator):
    def __init__(self, *validators):
        self._validators = validators

    def validate(self, ctx, value):
        errors = list()
        for val in self._validators:
            try:
                val.validate(ctx, value)
                return
            except ValidationError as err:
                errors.append(err.get_data())
        raise ValidationError("required at least 1 validator to pass", errors = errors)
