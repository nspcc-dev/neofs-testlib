import logging
import socket
import textwrap
from datetime import datetime
from functools import lru_cache, wraps
from time import sleep
from typing import ClassVar, Optional

from paramiko import (
    AutoAddPolicy,
    ECDSAKey,
    Ed25519Key,
    PKey,
    RSAKey,
    SSHClient,
    SSHException,
    ssh_exception,
)
from paramiko.ssh_exception import AuthenticationException

from neofs_testlib.reporter import get_reporter
from neofs_testlib.shell.interfaces import CommandOptions, CommandResult, Shell

logger = logging.getLogger("neofs.testlib.shell")
reporter = get_reporter()


class HostIsNotAvailable(Exception):
    """Raised when host is not reachable via SSH connection."""

    def __init__(self, host: str = None):
        msg = f"Host {host} is not available"
        super().__init__(msg)


def log_command(func):
    @wraps(func)
    def wrapper(shell: "SSHShell", command: str, *args, **kwargs) -> CommandResult:
        command_info = command.removeprefix("$ProgressPreference='SilentlyContinue'\n")
        with reporter.step(command_info):
            logging.info(f'Execute command "{command}" on "{shell.host}"')

            start_time = datetime.utcnow()
            result = func(shell, command, *args, **kwargs)
            end_time = datetime.utcnow()

            elapsed_time = end_time - start_time
            log_message = (
                f"HOST: {shell.host}\n"
                f"COMMAND:\n{textwrap.indent(command, ' ')}\n"
                f"RC:\n {result.return_code}\n"
                f"STDOUT:\n{textwrap.indent(result.stdout, ' ')}\n"
                f"STDERR:\n{textwrap.indent(result.stderr, ' ')}\n"
                f"Start / End / Elapsed\t {start_time.time()} / {end_time.time()} / {elapsed_time}"
            )

            logger.info(log_message)
            reporter.attach(log_message, "SSH command.txt")
        return result

    return wrapper


@lru_cache
def _load_private_key(file_path: str, password: Optional[str]) -> PKey:
    """Loads private key from specified file.

    We support several type formats, however paramiko doesn't provide functionality to determine
    key type in advance. So we attempt to load file with each of the supported formats and then
    cache the result so that we don't need to figure out type again on subsequent calls.
    """
    logger.debug(f"Loading ssh key from {file_path}")
    for key_type in (Ed25519Key, ECDSAKey, RSAKey):
        try:
            return key_type.from_private_key_file(file_path, password)
        except SSHException as ex:
            logger.warn(f"SSH key {file_path} can't be loaded with {key_type}: {ex}")
            continue
    raise SSHException(f"SSH key {file_path} is not supported")


class SSHShell(Shell):
    """Implements command shell on a remote machine via SSH connection."""

    # Time in seconds to delay after remote command has completed. The delay is required
    # to allow remote command to flush its output buffer
    DELAY_AFTER_EXIT = 0.2

    SSH_CONNECTION_ATTEMPTS: ClassVar[int] = 3
    CONNECTION_TIMEOUT = 90

    def __init__(
        self,
        host: str,
        login: str,
        password: Optional[str] = None,
        private_key_path: Optional[str] = None,
        private_key_passphrase: Optional[str] = None,
        port: str = "22",
    ) -> None:
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.private_key_path = private_key_path
        self.private_key_passphrase = private_key_passphrase
        self.__connection: Optional[SSHClient] = None

    @property
    def _connection(self):
        if not self.__connection:
            self.__connection = self._create_connection()
        return self.__connection

    def drop(self):
        self._reset_connection()

    def exec(self, command: str, options: Optional[CommandOptions] = None) -> CommandResult:
        options = options or CommandOptions()

        if options.interactive_inputs:
            result = self._exec_interactive(command, options)
        else:
            result = self._exec_non_interactive(command, options)

        if options.check and result.return_code != 0:
            raise RuntimeError(
                f"Command: {command}\nreturn code: {result.return_code}"
                f"\nOutput: {result.stdout}"
            )
        return result

    @log_command
    def _exec_interactive(self, command: str, options: CommandOptions) -> CommandResult:
        stdin, stdout, stderr = self._connection.exec_command(command, timeout=options.timeout)
        for interactive_input in options.interactive_inputs:
            input = interactive_input.input
            if not input.endswith("\n"):
                input = f"{input}\n"
            try:
                stdin.write(input)
            except OSError:
                logger.exception(f"Error while feeding {input} into command {command}")
        # stdin.close()

        # Wait for command to complete and flush its buffer before we attempt to read output
        sleep(self.DELAY_AFTER_EXIT)
        return_code = stdout.channel.recv_exit_status()
        sleep(self.DELAY_AFTER_EXIT)

        result = CommandResult(
            stdout=stdout.read().decode(errors="ignore"),
            stderr=stderr.read().decode(errors="ignore"),
            return_code=return_code,
        )
        return result

    @log_command
    def _exec_non_interactive(self, command: str, options: CommandOptions) -> CommandResult:
        try:
            _, stdout, stderr = self._connection.exec_command(command, timeout=options.timeout)

            # Wait for command to complete and flush its buffer before we attempt to read output
            return_code = stdout.channel.recv_exit_status()
            sleep(self.DELAY_AFTER_EXIT)

            return CommandResult(
                stdout=stdout.read().decode(errors="ignore"),
                stderr=stderr.read().decode(errors="ignore"),
                return_code=return_code,
            )
        except (
            SSHException,
            TimeoutError,
            ssh_exception.NoValidConnectionsError,
            ConnectionResetError,
            AttributeError,
            socket.timeout,
        ) as exc:
            logger.exception(f"Can't execute command {command} on host: {self.host}")
            self._reset_connection()
            raise HostIsNotAvailable(self.host) from exc

    def _create_connection(self, attempts: int = SSH_CONNECTION_ATTEMPTS) -> SSHClient:
        for attempt in range(attempts):
            connection = SSHClient()
            connection.set_missing_host_key_policy(AutoAddPolicy())
            try:
                if self.private_key_path:
                    logging.info(
                        f"Trying to connect to host {self.host} as {self.login} using SSH key "
                        f"{self.private_key_path} (attempt {attempt})"
                    )
                    connection.connect(
                        hostname=self.host,
                        port=self.port,
                        username=self.login,
                        pkey=_load_private_key(self.private_key_path, self.private_key_passphrase),
                        timeout=self.CONNECTION_TIMEOUT,
                    )
                else:
                    logging.info(
                        f"Trying to connect to host {self.host} as {self.login} using password "
                        f"(attempt {attempt})"
                    )
                    connection.connect(
                        hostname=self.host,
                        port=self.port,
                        username=self.login,
                        password=self.password,
                        timeout=self.CONNECTION_TIMEOUT,
                    )
                return connection
            except AuthenticationException:
                connection.close()
                logger.exception(f"Can't connect to host {self.host}")
                raise
            except (
                SSHException,
                ssh_exception.NoValidConnectionsError,
                AttributeError,
                socket.timeout,
                OSError,
            ) as exc:
                connection.close()
                can_retry = attempt + 1 < attempts
                if can_retry:
                    logger.warn(f"Can't connect to host {self.host}, will retry. Error: {exc}")
                    continue
                logger.exception(f"Can't connect to host {self.host}")
                raise HostIsNotAvailable(self.host) from exc

    def _reset_connection(self) -> None:
        if self.__connection:
            self.__connection.close()
        self.__connection = None
