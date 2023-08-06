from .type import TypeValidator
from .base import Validator

class NoneValidator(Validator):
    def validate(self, ctx, value):
        TypeValidator(type(None)).validate(ctx, value)