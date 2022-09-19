from cli.cli_command import NeofsCliCommand
from shell import CommandResult


class NeofsAdmStorageConfig(NeofsCliCommand):
    def set(self, account: str, wallet: str) -> CommandResult:
        """Initialize basic neofs-adm configuration file.

        Args:
            account (str):  wallet account
            wallet (str):   path to wallet


        Returns:
            str: Command string

        """
        return self._execute(
            "storage-config",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            }
        )
