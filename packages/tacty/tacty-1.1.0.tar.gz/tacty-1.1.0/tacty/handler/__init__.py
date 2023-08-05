from abc import ABC, abstractclassmethod


class Handler(ABC):
    @abstractclassmethod
    def handle(self, command: object) -> any:
        pass
