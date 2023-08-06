from .str import StrValidator
from .base import Validator
from email.utils import parseaddr

class EmailValidator(Validator):
    def validate(self, ctx, value):
        StrValidator().validate(ctx, value)
        if len(parseaddr(value)[1]) == 0:
            ctx.error("value is not an email", value = value)