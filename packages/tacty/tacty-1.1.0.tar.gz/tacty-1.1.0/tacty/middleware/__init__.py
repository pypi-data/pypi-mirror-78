from abc import ABC, abstractclassmethod
from typing import Callable

from tacty.resolver import Resolver


class Middleware(ABC):
    @abstractclassmethod
    def execute(self, command: object, next: Callable) -> any:
        pass


class CommandHandlerMiddleware(Middleware):
    def __init__(self, resolver: Resolver) -> None:
        self.resolver: Resolver = resolver

    def execute(self, command: object, next: Callable) -> any:
        handler = self.resolver.resolve(type(command))
        return handler.handle(command)
