from abc import ABC, abstractmethod
from exceptions import ToolValidationError, ToolValidationMissError


class BaseTool(ABC):
    name: str
    description: str
    schema: dict

    def validate(self, args: dict):
        if not isinstance(args, dict):
            raise ToolValidationError("Arguments must be a dictionary")

        for field in self.schema["required"]:
            if field not in args:
                raise ToolValidationMissError(f"Missing required field: {field}")

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
