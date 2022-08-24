from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Any


class Reporter(ABC):
    """
    Interface that supports storage of test artifacts in some reporting tool.
    """

    @abstractmethod
    def step(self, name: str) -> AbstractContextManager:
        """
        Register a new step in test execution.

        :param str name: Name of the step
        :return: step context
        """
        pass

    @abstractmethod
    def attach(self, content: Any, file_name: str) -> None:
        """
        Attach specified content with given file name to the test report.

        :param any name: content to attach. If not a string, it will be converted to a string.
        :param str file_name: file name of attachment.
        """
        pass
