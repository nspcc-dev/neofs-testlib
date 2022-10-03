# neofs-testlib
This library provides building blocks and utilities to facilitate development of automated tests for NeoFS system.

## Installation
Library can be installed via pip:
```shell
$ pip install neofs-testlib
```

## Configuration
Library components can be configured explicitly via code or implicitly via configuration file that supports plugin-based extensions.

By default testlib uses configuration from file `.neofs-testlib.yaml` that must be located next to the process entry point. Path to the file can be customized via environment variable `NEOFS_TESTLIB_CONFIG`. Config file should have either YAML or JSON format.

### Reporter Configuration
Currently only reporter component can be configured. Function `set_reporter` assigns current reporter that should be used in the library:

```python
from neofs_testlib.reporter import AllureReporter, set_reporter

reporter = AllureReporter()
set_reporter(reporter)
```

Assignment of reporter must happen before any testlib modules were imported. Otherwise, testlib code will bind to default dummy reporter. It is not convenient to call utility functions at specific time, so alternative approach is to set reporter in configuration file. To do that, please, specify name of reporter plugin in configuration parameter `reporter`:
```yaml
reporter: allure
```

Testlib provides two built-in reporters: `allure` and `dummy`. However, you can use any custom reporter via [plugins](#plugins).

## Plugins
Testlib uses [entrypoint specification](https://docs.python.org/3/library/importlib.metadata.html) for plugins. Testlib supports the following entrypoint groups for plugins:
 - `neofs.testlib.reporter` - group for reporter plugins. Plugin should be a class that implements interface `neofs_testlib.reporter.interfaces.Reporter`.

### Example reporter plugin
In this example we will consider two Python projects:
 - Project "my_neofs_plugins" where we will build a plugin that extends testlib functionality.
 - Project "my_neofs_tests" that uses "neofs_testlib" and "my_neofs_plugins" to build some tests.

Let's say we want to implement some custom reporter that can be used as a plugin for testlib. Pseudo-code of implementation can look like that:
```python
# my_neofs_plugins/src/x/y/z/custom_reporter.py
from contextlib import AbstractContextManager
from neofs_testlib.reporter.interfaces import Reporter


class CustomReporter(Reporter):
    def step(self, name: str) -> AbstractContextManager:
        ... some implementation ...

    def attach(self, content: Any, file_name: str) -> None:
        ... some implementation ...
```

Then in `pyproject.toml` of "my_neofs_plugins" we should register entrypoint for this plugin. Entrypoint must belong to the group `neofs.testlib.reporter`:
```yaml
# my_neofs_plugins/pyproject.toml
[project.entry-points."neofs.testlib.reporter"]
my_custom_reporter = "x.y.z.custom_reporter:CustomReporter"
```

Finally, to use this reporter in our test project "my_neofs_tests", we should specify its entrypoint name in testlib config:
```yaml
# my_neofs_tests/pyproject.toml
reporter: my_custom_reporter
```

Detailed information on registering entrypoints can be found at [setuptools docs](https://setuptools.pypa.io/en/latest/userguide/entry_point.html).

## Library structure
The library provides the following primary components:
 * `cli` - wrappers on top of neoFS command-line tools. These wrappers execute on a shell and provide type-safe interface for interacting with the tools.
 * `reporter` - abstraction on top of test reporting tool like Allure. Components of the library will report their steps and attach artifacts to the configured reporter instance.
 * `shell` - shells that can be used to execute commands. Currently library provides local shell (on machine that runs the code) or SSH shell that connects to a remote machine via SSH.

## Contributing
Any contributions to the library should conform to the [contribution guideline](https://github.com/nspcc-dev/neofs-testlib/blob/master/CONTRIBUTING.md).
