from .str import StrValidator
from .base import Validator
from validate_email import validate_email

class EmailValidator(Validator):
    def validate(self, ctx, value):
        StrValidator().validate(ctx, value)
        if not validate_email(value):
            ctx.error("value is not an email", value = value)