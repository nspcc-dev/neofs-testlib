import traceback


def format_error_details(error: Exception) -> str:
    return "".join(traceback.format_exception(
        etype=type(error),
        value=error,
        tb=error.__traceback__)
    )
