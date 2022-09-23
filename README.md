# neofs-testlib
This library provides building blocks and utilities to facilitate development of automated tests for NeoFS system.

## Installation
Library can be installed via pip:
```shell
$ pip install neofs-testlib
```

## Library structure
The library provides the following primary components:
 * `cli` - wrappers on top of neoFS command-line tools. These wrappers execute on a shell and provide type-safe interface for interacting with the tools.
 * `reporter` - abstraction on top of test reporting tool like Allure. Components of the library will report their steps and attach artifacts to the configured reporter instance.
 * `shell` - shells that can be used to execute commands. Currently library provides local shell (on machine that runs the code) or SSH shell that connects to a remote machine via SSH.

## Contributing
Any contributions to the library should conform to the [contribution guideline](https://github.com/nspcc-dev/neofs-node/blob/master/CONTRIBUTING.md).

### Development Environment
To setup development environment for `neofs-testlib`, please, take the following steps:
1. Prepare virtualenv

```shell
$ virtualenv --python=python3.9 venv
$ source venv/bin/activate
```

2. Install all dependencies:

```shell
$ pip install -r requirements.txt
```

3. Setup pre-commit hooks to run code formatters on staged files before you run a `git commit` command:

```shell
$ pre-commit install
```

Optionally you might want to integrate code formatters with your code editor to apply formatters to code files as you go:
* isort is supported by [PyCharm](https://plugins.jetbrains.com/plugin/15434-isortconnect), [VS Code](https://cereblanco.medium.com/setup-black-and-isort-in-vscode-514804590bf9). Plugins exist for other IDEs/editors as well.
* black can be integrated with multiple editors, please, instructions are available [here](https://black.readthedocs.io/en/stable/integrations/editors.html).

### Unit Tests
Before submitting any changes to the library, please, make sure that all unit tests are passing. To run the tests, please, use the following command:
```shell
$ python -m unittest discover --start-directory tests
```

To enable tests that interact with SSH server, please, setup SSH server and set the following environment variables before running the tests:
```
SSH_SHELL_HOST = <address of the server>
SSH_SHELL_LOGIN = <login that has permissions to run python3 on the server>
SSH_SHELL_PRIVATE_KEY_PATH = <path to SSH private key on your machine>
SSH_SHELL_PRIVATE_KEY_PASSPHRASE = <passphrase for the SSH private key>
```

### Editable installation
If you would like to modify code of the library in the integration with your test suite, you can use editable installation. For that, in virtual environment of your test suite (not in the virtual environment of the testlib itself!) run the following command (path to `neofs-testlib` directory might be different on your machine):
```shell
$ pip install -e ../neofs-testlib
```

### Building and publishing package
To build Python package of the library, please run the following command in the library root directory:
```shell
$ python -m build
```

This command will put wheel file and source archive under `dist` directory.

To check that package description will be correctly rendered at PyPI, please, use command:
```shell
$ twine check dist/*
```

To upload package to [test PyPI](https://test.pypi.org/project/neofs-testlib/), please, use command:
```shell
$ twine upload -r testpypi dist/*
```
It will prompt for your username and password. You would need to [create test PyPI account](https://test.pypi.org/account/register/) in order to execute it.

To upload package to actual PyPI, please, use command:
```shell
$ twine upload dist/*
```
It will prompt for your username and password. You would need to [create PyPI account](https://pypi.org/account/register/) in order to execute it.
