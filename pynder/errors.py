class PynderError(Exception):
    pass


class RequestError(PynderError):
    pass


class InitializationError(PynderError):
    pass


class RecsError(PynderError):
    pass


class RecsTimeout(RecsError):
    pass
