from cli.cli_command import NeofsCliCommand
from shell import CommandResult


class NeofsAdmConfig(NeofsCliCommand):
    def init(self, path: str = "~/.neofs/adm/config.yml") -> CommandResult:
        """Initialize basic neofs-adm configuration file.

        Args:
            path (str):  path to config (default ~/.neofs/adm/config.yml)


        Returns:
            str: Command string

        """
        return self._execute(
            "config init",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            }
        )
