# neofs-testlib
This library provides building blocks and utilities to facilitate development of automated tests for NeoFS system.

## Repository structure
TODO

## Installation
TODO

## Contributing
Any contributions to the library should conform to the [contribution guideline](https://github.com/nspcc-dev/neofs-node/blob/master/CONTRIBUTING.md).

### Development Environment
To setup development environment for `neofs-testlib`, please, take the following steps:
1. Prepare virtualenv

```
$ virtualenv --python=python3.9 venv
$ source venv/bin/activate
```

2. Install all dependencies:

```
$ pip install -r requirements.txt
```

3. Setup pre-commit hooks to run code formatters on staged files before you run a `git commit` command:

```
pre-commit install
```

Optionally you might want to integrate code formatters with your code editor to apply formatters to code files as you go:
* isort is supported by [PyCharm](https://plugins.jetbrains.com/plugin/15434-isortconnect), [VS Code](https://cereblanco.medium.com/setup-black-and-isort-in-vscode-514804590bf9). Plugins exist for other IDEs/editors as well.
* black can be integrated with multiple editors, please, instructions are available [here](https://black.readthedocs.io/en/stable/integrations/editors.html).

### Unit Tests
Before submitting any changes to the library, please, make sure that all unit tests are passing. To run the tests, please, use the following command:
```
python -m unittest discover --start-directory tests
```

To enable tests that interact with SSH server, please, setup SSH server and set the following environment variables before running the tests:
```
SSH_SHELL_HOST = <address of the server>
SSH_SHELL_LOGIN = <login that has permissions to run python3 on the server>
SSH_SHELL_PRIVATE_KEY_PATH = <path to SSH private key on your machine>
SSH_SHELL_PRIVATE_KEY_PASSPHRASE = <passphrase for the SSH private key>
```