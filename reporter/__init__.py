import os

from .allure_reporter import AllureReporter
from .interfaces import Reporter
from .dummy_reporter import DummyReporter


def get_reporter() -> Reporter:
    # TODO: in scope of reporter implementation task here we will have extendable
    # solution for configuring and providing reporter for the library
    if os.getenv("TESTLIB_REPORTER_TYPE", "DUMMY") == "DUMMY":
        return DummyReporter()
    else:
        return AllureReporter()
