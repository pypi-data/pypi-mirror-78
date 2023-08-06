from .error import ValidationError

class Context:
    def __init__(self, path = ["$"]):
        self._path = path

    def __getitem__(self, key):
        return Context(self._path + [ key ])

    def get_path(self):
        return ".".join(str(x) for x in self._path)

    def error(self, msg, ** kwargs):
        raise ValidationError(msg, path = self.get_path(), ** kwargs)

class Validator:
    def __call__(self, value):
        ctx = Context()
        self.validate(ctx, value)