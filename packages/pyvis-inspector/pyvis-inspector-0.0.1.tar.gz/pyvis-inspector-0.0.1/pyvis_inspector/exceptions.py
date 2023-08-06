

class PyvisException(IOError):

    def __init__(self):
        pass


class TokenError(PyvisException):
    """A Token Error Occurred"""
