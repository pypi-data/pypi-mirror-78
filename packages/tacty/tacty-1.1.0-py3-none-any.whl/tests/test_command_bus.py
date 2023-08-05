import unittest

from typing import Callable
from unittest.mock import Mock
from unittest.mock import call

from tacty.middleware import Middleware
from tacty.command_bus import CommandBus


class FirstMiddleware(Middleware):
    def execute(self, command: object, next: Callable) -> any:
        command.middleware_call('first_middleware')
        next(command)


class SecondMiddleware(Middleware):
    def execute(self, command: object, next: Callable) -> any:
        command.middleware_call('second_middleware')
        next(command)


class LasttMiddleware(Middleware):
    def execute(self, command: object, next: Callable) -> any:
        command.middleware_call('last_middleware')


class TestCommandBus(unittest.TestCase):
    def test_middlewares_are_executed_in_order(self):
        # Arrange
        command_bus = CommandBus(
            [FirstMiddleware(), SecondMiddleware(), LasttMiddleware()]
        )

        expected_middleware_calls = [
            call('first_middleware'),
            call('second_middleware'),
            call('last_middleware')
        ]

        # Act
        test_command = Mock()
        test_command.middleware_call = Mock()
        command_bus.handle(test_command)

        # Assert
        test_command.middleware_call.assert_has_calls(
            expected_middleware_calls
        )
