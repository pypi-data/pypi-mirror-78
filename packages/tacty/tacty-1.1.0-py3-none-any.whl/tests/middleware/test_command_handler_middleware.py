import unittest
from unittest.mock import Mock, patch

from tacty.handler import Handler
from tacty.middleware import CommandHandlerMiddleware


class TestCommand:
    def __init__(self, value: int = 1000):
        self.value = value


class TestHandler(Handler):
    def handle(self, command: TestCommand) -> None:
        return command.value


class TestCommandHandlerMiddleware(unittest.TestCase):
    @patch('tacty.resolver.Resolver')
    def test_commands_are_resolved_using_the_resolver(self, mock_resolver):
        # Arrange
        test_command = TestCommand()
        mock_resolver.resolve = Mock()

        # Act
        middleware = CommandHandlerMiddleware(mock_resolver)
        middleware.execute(test_command, lambda *args: None)

        # Assert
        mock_resolver.resolve.assert_called_with(type(test_command))

    @patch('tacty.resolver.Resolver')
    def test_handler_gets_executed(self, mock_resolver):
        # Arrange
        test_command = TestCommand()
        mock_test_handler = Mock()
        mock_test_handler.handle = Mock()
        mock_resolver.resolve = Mock()
        mock_resolver.resolve.return_value = mock_test_handler

        # Act
        middleware = CommandHandlerMiddleware(mock_resolver)
        middleware.execute(test_command, lambda *args: None)

        # Assert
        mock_test_handler.handle.assert_called_once_with(test_command)

    @patch('tacty.resolver.Resolver')
    def test_handler_returned_value_is_returned(self, mock_resolver):
        # Arrange
        test_command = TestCommand(2000)
        mock_resolver.resolve = Mock()
        mock_resolver.resolve.return_value = TestHandler()

        # Act
        middleware = CommandHandlerMiddleware(mock_resolver)
        return_value = middleware.execute(test_command, lambda *args: None)

        # Assert
        self.assertEqual(return_value, test_command.value)
