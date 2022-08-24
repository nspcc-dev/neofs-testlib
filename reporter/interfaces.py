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

    @abstractmethod
    def attach(self, content: Any, file_name: str) -> None:
        """
        Attach specified content with given file name to the test report.

        :param any content: content to attach. If content value is not a string, it will be
        converted to a string.
        :param str file_name: file name of attachment.
        """
