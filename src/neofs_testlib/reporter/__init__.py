import os

from neofs_testlib.reporter.allure_reporter import AllureReporter
from neofs_testlib.reporter.dummy_reporter import DummyReporter
from neofs_testlib.reporter.interfaces import Reporter


def get_reporter() -> Reporter:
    # TODO: in scope of reporter implementation task here we will have extendable
    # solution for configuring and providing reporter for the library
    if os.getenv("TESTLIB_REPORTER_TYPE", "DUMMY") == "DUMMY":
        return DummyReporter()
    else:
        return AllureReporter()
