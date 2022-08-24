import os

from reporter.allure_reporter import AllureReporter
from reporter.dummy_reporter import DummyReporter
from reporter.interfaces import Reporter


def get_reporter() -> Reporter:
    # TODO: in scope of reporter implementation task here we will have extendable
    # solution for configuring and providing reporter for the library
    if os.getenv("TESTLIB_REPORTER_TYPE", "DUMMY") == "DUMMY":
        return DummyReporter()
    else:
        return AllureReporter()
