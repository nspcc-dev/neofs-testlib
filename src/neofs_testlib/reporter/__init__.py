from neofs_testlib.reporter.allure_reporter import AllureReporter
from neofs_testlib.reporter.dummy_reporter import DummyReporter
from neofs_testlib.reporter.interfaces import Reporter

__reporter = DummyReporter()


def get_reporter() -> Reporter:
    """
    Returns reporter that library should use for storing artifacts.
    """
    return __reporter


def set_reporter(reporter: Reporter) -> None:
    """
    Assigns specified reporter for storing test artifacts produced by the library.

    This function must be called before any testlib modules are imported.
    Recommended way to assign reporter is via configuration file; please, refer to
    testlib documentation for details.
    """
    global __reporter
    __reporter = reporter
