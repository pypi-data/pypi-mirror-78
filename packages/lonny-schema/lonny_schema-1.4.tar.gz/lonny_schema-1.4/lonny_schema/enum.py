from .base import Validator
from .type import TypeValidator

class EnumValidator:
    def __init__(self, enum):
        self._enum = enum

    def validate(self, ctx, value):
        TypeValidator(str).validate(ctx, value)
        if value not in self._enum:
            ctx.error("value is not a valid member", value = value)