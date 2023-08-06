class ValidationError(Exception):
    def __init__(self, message, *, path = None, **kwargs ):
        super().__init__(message)
        self._path = path
        self._kwargs = kwargs

    def get_data(self):
        serialized = dict(error = str(self))
        if self._path is not None:
            serialized["path"] = self._path
        if len(self._kwargs) > 0:
            serialized["details"] = self._kwargs
        return serialized