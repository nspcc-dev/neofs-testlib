from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class InteractiveInput:
    """Interactive input for a shell command.

    Attributes:
        prompt_pattern: regular expression that defines expected prompt from the command.
        input: user input that should be supplied to the command in response to the prompt.
    """

    prompt_pattern: str
    input: str


@dataclass
class CommandOptions:
    """Options that control command execution.

    Attributes:
        interactive_inputs: user inputs that should be interactively supplied to
            the command during execution.
        timeout: timeout for command execution (in seconds).
        check: controls whether to check return code of the command. Set to False to
            ignore non-zero return codes.
    """

    interactive_inputs: Optional[list[InteractiveInput]] = None
    timeout: int = 30
    check: bool = True


@dataclass
class CommandResult:
    """Represents a result of a command executed via shell.

    Attributes:
        stdout: complete content of stdout stream.
        stderr: complete content of stderr stream.
        return_code: return code (or exit code) of the command's process.
    """

    stdout: str
    stderr: str
    return_code: int


class Shell(ABC):
    """Interface of a command shell on some system (local or remote)."""

    @abstractmethod
    def exec(self, command: str, options: Optional[CommandOptions] = None) -> CommandResult:
        """Executes specified command on this shell.

        To execute interactive command, user inputs should be specified in *options*.

        Args:
            command: Command to execute on the shell.
            options: Options that control command execution.

        Returns:
            Command's result.
        """
