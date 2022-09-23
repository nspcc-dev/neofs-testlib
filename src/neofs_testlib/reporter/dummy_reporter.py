from contextlib import AbstractContextManager, contextmanager
from typing import Any

from neofs_testlib.reporter.interfaces import Reporter


@contextmanager
def _dummy_step():
    yield


class DummyReporter(Reporter):
    """
    Dummy implementation of reporter, does not store artifacts anywhere.
    """

    def step(self, name: str) -> AbstractContextManager:
        return _dummy_step()

    def attach(self, content: Any, file_name: str) -> None:
        pass
