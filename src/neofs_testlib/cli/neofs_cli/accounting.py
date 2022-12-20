from typing import Optional, Union

from neofs_testlib.cli.cli_command import CliCommand
from neofs_testlib.shell import CommandResult


class NeofsCliAccounting(CliCommand):
    def balance(
        self,
        wallet: Optional[str] = None,
        parse_result=False,
        rpc_endpoint: Optional[str] = None,
        address: Optional[str] = None,
        owner: Optional[str] = None,
    ) -> Union[int, CommandResult]:
        """Get internal balance of NeoFS account

        Args:
            address: Address of wallet account.
            parse_result: Return parsed balance
            owner: Owner of balance account (omit to use owner from private key).
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            wallet: WIF (NEP-2) string or path to the wallet or binary key.

        Returns:
            Account balance or Command's result.

        """
        result = self._execute(
            "accounting balance",
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "parse_result"]
            },
        )
        if not parse_result:
            return result

        return int(result.stdout.strip())
