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
Any contributions to the library should conform to the [contribution guideline](https://github.com/nspcc-dev/neofs-testlib/blob/master/CONTRIBUTING.md).
