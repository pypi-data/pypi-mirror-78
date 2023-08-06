from .base import Validator

class DummyValidator(Validator):
    def validate(self, ctx, value):
        pass