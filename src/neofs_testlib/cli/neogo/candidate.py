from typing import Optional

from neofs_testlib.cli.cli_command import CliCommand
from neofs_testlib.shell import CommandResult


class NeoGoCandidate(CliCommand):
    def register(
        self,
        address: str,
        rpc_endpoint: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        gas: Optional[float] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Register as a new candidate.

        Args:
            address: Address to register.
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            gas: Network fee to add to the transaction (prioritizing it).
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet candidate register",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def unregister(
        self,
        address: str,
        rpc_endpoint: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        gas: Optional[float] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Unregister self as a candidate.

        Args:
            address: Address to unregister.
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            gas: Network fee to add to the transaction (prioritizing it).
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet candidate unregister",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def vote(
        self,
        candidate: str,
        rpc_endpoint: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        gas: Optional[float] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Votes for a validator.

        Voting happens by calling "vote" method of a NEO native contract. Do not provide
        candidate argument to perform unvoting.

        Args:
            candidate: Public key of candidate to vote for.
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            gas: Network fee to add to the transaction (prioritizing it).
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet candidate vote",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )
