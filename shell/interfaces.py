from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class InteractiveInput:
    """
    Interactive input for a shell command.

    :attr str prompt_pattern: regular expression that defines expected prompt from the command.
    :attr str input: user input that should be supplied to the command in response to the prompt.
    """

    prompt_pattern: str
    input: str


@dataclass
class CommandOptions:
    """
    Options that control command execution.

    :attr list interactive_inputs: user inputs that should be interactively supplied to
          the command during its' execution.
    :attr int timeout: timeout for command execution (in seconds).
    :attr bool check: controls whether to check return code of the command. Set to False to
          ignore non-zero return codes.
    """

    interactive_inputs: Optional[list[InteractiveInput]] = None
    timeout: int = 30
    check: bool = True


@dataclass
class CommandResult:
    """
    Represents a result of a command executed via shell.
    """

    stdout: str
    stderr: str
    return_code: int


class Shell(ABC):
    """
    Interface of a command shell on some system (local or remote).
    """

    @abstractmethod
    def exec(self, command: str, options: Optional[CommandOptions] = None) -> CommandResult:
        """
        Executes specified command on this shell. To execute interactive command, user inputs
        should be specified in *options*.

        :param str command: command to execute on the shell.
        :param CommandOptions options: options that control command execution.
        :return command result.
        """
