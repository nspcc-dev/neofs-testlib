from neofs_testlib.cli.cli_command import CliCommand
from neofs_testlib.cli.neogo.network_type import NetworkType
from neofs_testlib.shell import CommandResult


class NeoGoNode(CliCommand):
    def start(self, network: NetworkType = NetworkType.PRIVATE) -> CommandResult:
        """Start a NEO node

        Args:
            network (NetworkType): Select network type (default: private)

        Returns:
            str: Command string

        """
        return self._execute("start", **{network.value: True})
