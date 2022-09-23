import traceback

from neofs_testlib.shell.interfaces import CommandResult


def format_error_details(error: Exception) -> str:
    """
    Converts specified exception instance into a string that includes error message
    and full stack trace.

    :param Exception error: exception to convert.
    :return: string containing exception details.
    """
    detail_lines = traceback.format_exception(
        etype=type(error),
        value=error,
        tb=error.__traceback__,
    )
    return "".join(detail_lines)


def get_output_lines(result: CommandResult) -> list[str]:
    """
    Converts output of specified command result into separate lines trimmed from whitespaces.
    Empty lines are excluded.

    :param CommandResult result: result which output should be converted.
    :return: list of lines extracted from the output.
    """
    return [line.strip() for line in result.stdout.split("\n") if line.strip()]
