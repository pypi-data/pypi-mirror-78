from abc import ABC, abstractclassmethod
from typing import Dict

from tacty.exception import (
    HandlerForCommandAlreadyExistsError,
    HandlerForCommandDoesNotExistError,
    HandlerIsNotAHandlerSubClassError,
)
from tacty.handler import Handler


class Resolver(ABC):
    @abstractclassmethod
    def resolve(self, command: type) -> Handler:
        pass


class InMemoryResolver(Resolver):
    def __init__(self) -> None:
        self.handlers: Dict = {}

    def add_handler(self, command: type, handler: Handler) -> None:
        if not issubclass(handler.__class__, Handler):
            raise HandlerIsNotAHandlerSubClassError()

        if command in self.handlers.keys():
            raise HandlerForCommandAlreadyExistsError()

        self.handlers[command] = handler

    def resolve(self, command: type) -> Handler:
        if command not in self.handlers.keys():
            raise HandlerForCommandDoesNotExistError()

        return self.handlers[command]
