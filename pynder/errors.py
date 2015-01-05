class PynderError(Exception):
    pass


class RequestError(PynderError):
    pass


class InitializationError(PynderError):
    pass
