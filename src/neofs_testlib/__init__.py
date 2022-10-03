import json
import os
import sys
from typing import Any, Optional

import yaml

from neofs_testlib.reporter import set_reporter

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points


__version__ = "0.1.0"


def __read_config() -> dict[str, Any]:
    """
    Loads configuration of library from default file .neofs-testlib.yaml or from
    the file configured via environment variable NEOFS_TESTLIB_CONFIG.
    """
    file_path = os.getenv("NEOFS_TESTLIB_CONFIG", ".neofs-testlib.yaml")
    if os.path.exists(file_path):
        _, extension = os.path.splitext(file_path)
        if extension == ".yaml":
            with open(file_path, "r") as file:
                return yaml.full_load(file)
        if extension == ".json":
            with open(file_path, "r") as file:
                return json.load(file)
    return {}


def __load_plugin(group: str, name: Optional[str]) -> Any:
    """
    Loads plugin using entry point specification.
    """
    if not name:
        return None
    plugins = entry_points(group=group)
    if name not in plugins.names:
        return None
    plugin = plugins[name]
    return plugin.load()


def __init_lib():
    """
    Initializes singleton components in the library.
    """
    config = __read_config()

    reporter = __load_plugin("neofs.testlib.reporter", config.get("reporter"))
    if reporter:
        set_reporter(reporter)


__init_lib()
