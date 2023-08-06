from .type import TypeValidator
from .base import Validator

class DictValidator(Validator):
    def __init__(self, * validators, allow_others = False):
        self._validators = validators
        self._allow_others = allow_others

    def validate(self, ctx, value):
        TypeValidator(dict).validate(ctx, value)
        keys = set()
        for validator in self._validators:
            row = { ix : x for ix, x in enumerate(validator) }
            keys.add(row[0])
            if row[0] not in value:
                if not row.get(2, True):
                    continue
                ctx.error("Missing required key", key = row[0])
            row[1].validate(ctx[row[0]], value[row[0]])
        for key in value.keys():
            if key not in keys and not self._allow_others:
                ctx.error("Unexpected key", key = key)