from .type import TypeValidator
from .base import Validator

class BoolValidator(Validator):
    def validate(self, ctx, value):
        TypeValidator(bool).validate(ctx, value)