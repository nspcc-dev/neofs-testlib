from neofs_testlib.cli.cli_command import CliCommand
from neofs_testlib.shell import CommandResult


class NeofsAdmConfig(CliCommand):
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
            },
        )
