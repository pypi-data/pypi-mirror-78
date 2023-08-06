from .str import StrValidator
from .base import Validator
from phonenumbers import parse, is_valid_number
from phonenumbers.phonenumberutil import NumberParseException

class E164Validator(Validator):

    def _is_valid(self, value):
        if any(x for x in value if x.isalpha()):
            return False
        try:
            parsed = parse(value)
            if not is_valid_number(parsed):
                return False
        except NumberParseException:
            return False
        return True

    def validate(self, ctx, value):
        StrValidator().validate(ctx, value)
        if not self._is_valid(value):
            ctx.error("value is not a e.164 phone number", value = value)
