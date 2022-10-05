from neofs_testlib.cli.cli_command import CliCommand
from neofs_testlib.shell import CommandResult


class NeofsAdmStorageConfig(CliCommand):
    def set(self, account: str, wallet: str) -> CommandResult:
        """Initialize basic neofs-adm configuration file.

        Args:
            account: Wallet account.
            wallet: Path to wallet.

        Returns:
            Command's result.
        """
        return self._execute(
            "storage-config",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )
