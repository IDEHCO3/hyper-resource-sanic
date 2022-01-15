class PathError(SyntaxError):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code


class ParentheseError(SyntaxError):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code