from abc import ABC, abstractmethod


class BaseTool(ABC):
    name: str
    description: str
    schema: dict

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
