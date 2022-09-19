from cli.cli_command import NeofsCliCommand
from shell import CommandResult

from .blockchain_network_type import NetworkType


class NeoGoNode(NeofsCliCommand):
    def start(self, network: NetworkType = NetworkType.PRIVATE) -> CommandResult:
        """Start a NEO node

        Args:
            network (NetworkType): Select network type (default: private)

        Returns:
            str: Command string

        """
        return self._execute("start", **{network.value: True})
