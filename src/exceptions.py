class ToolValidationMissError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class ParserError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class ToolValidationError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class ToolExecutionError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class LLMError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

class ToolNotFoundError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
        
