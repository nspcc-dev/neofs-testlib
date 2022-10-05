from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from neofs_testlib.hosting.config import CLIConfig, HostConfig, ServiceConfig
from neofs_testlib.shell.interfaces import Shell


class Host(ABC):
    """Interface of a host machine where neoFS services are running.

    Allows to manage the machine and neoFS services that are hosted on it.
    """

    def __init__(self, config: HostConfig) -> None:
        self._config = config
        self._service_config_by_name = {
            service_config.name: service_config for service_config in config.services
        }
        self._cli_config_by_name = {cli_config.name: cli_config for cli_config in config.clis}

    @property
    def config(self) -> HostConfig:
        """Returns config of the host.

        Returns:
            Config of this host.
        """
        return self._config

    def get_service_config(self, service_name: str) -> ServiceConfig:
        """Returns config of service with specified name.

        The service must be hosted on this host.

        Args:
            service_name: Name of the service.

        Returns:
            Config of the service.
        """
        service_config = self._service_config_by_name.get(service_name)
        if service_config is None:
            raise ValueError(f"Unknown service name: '{service_name}'")
        return service_config

    def get_cli_config(self, cli_name: str) -> CLIConfig:
        """Returns config of CLI tool with specified name.

        The CLI must be located on this host.

        Args:
            cli_name: Name of the CLI tool.

        Returns:
            Config of the CLI tool.
        """
        cli_config = self._cli_config_by_name.get(cli_name)
        if cli_config is None:
            raise ValueError(f"Unknown CLI name: '{cli_name}'")
        return cli_config

    @abstractmethod
    def get_shell(self) -> Shell:
        """Returns shell to this host.

        Returns:
            Shell that executes commands on this host.
        """

    @abstractmethod
    def start_host(self) -> None:
        """Starts the host machine."""

    @abstractmethod
    def stop_host(self, mode: str) -> None:
        """Stops the host machine.

        Args:
            mode: Specifies mode how host should be stopped. Mode might be host-specific.
        """

    @abstractmethod
    def start_service(self, service_name: str) -> None:
        """Starts the service with specified name and waits until it starts.

        The service must be hosted on this host.

        Args:
            service_name: Name of the service to start.
        """

    @abstractmethod
    def stop_service(self, service_name: str) -> None:
        """Stops the service with specified name and waits until it stops.

        The service must be hosted on this host.

        Args:
            service_name: Name of the service to stop.
        """

    @abstractmethod
    def delete_storage_node_data(self, service_name: str) -> None:
        """Erases all data of the storage node with specified name.

        Args:
            service_name: Name of storage node service.
        """

    @abstractmethod
    def dump_logs(
        self,
        directory_path: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> None:
        """Dumps logs of all services on the host to specified directory.

        Args:
            directory_path: Path to the directory where logs should be stored.
            since: If set, limits the time from which logs should be collected. Must be in UTC.
            until: If set, limits the time until which logs should be collected. Must be in UTC.
        """
