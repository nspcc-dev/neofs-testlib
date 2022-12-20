import re
from typing import Optional, Union

from neofs_testlib.cli.cli_command import CliCommand
from neofs_testlib.models import StorageGroup
from neofs_testlib.shell import CommandResult


class NeofsCliStorageGroup(CliCommand):
    GET_REGEX = re.compile(
        r"Expiration epoch: (?P<expiration_epoch>\d+)\n"
        r"Group size: (?P<group_size>\d+)\n"
        r"Group hash: (?P<group_hash>.+)\n"
        r"Members:\n"
        r"(?P<members>(\t\w+\n)*)"
    )

    def put(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        members: list[str],
        ttl: Optional[int] = None,
        bearer: Optional[str] = None,
        lifetime: Optional[int] = None,
        address: Optional[str] = None,
        xhdr: Optional[dict] = None,
    ) -> CommandResult:
        """
        Put storage group to NeoFS.

        Args:
            address: Address of wallet account.
            bearer: File with signed JSON or binary encoded bearer token.
            cid: Container ID.
            members: ID list of storage group members.
            lifetime: Storage group lifetime in epochs.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header.
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        members = ",".join(members)
        return self._execute(
            "storagegroup put",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def get(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        id: str,
        parse_result: bool = False,
        raw: Optional[bool] = False,
        ttl: Optional[int] = None,
        bearer: Optional[str] = None,
        lifetime: Optional[int] = None,
        address: Optional[str] = None,
        xhdr: Optional[dict] = None,
    ) -> Union[StorageGroup, CommandResult]:
        """
        Get storage group from NeoFS.

        Args:
            address: Address of wallet account.
            bearer: File with signed JSON or binary encoded bearer token.
            cid: Container ID.
            parse_result: Return storage group object.
            id: Storage group identifier.
            raw: Set raw request option.
            lifetime: Storage group lifetime in epochs.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header.
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        result = self._execute(
            "storagegroup get",
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "parse_result"]
            },
        )
        if not parse_result:
            return result
        storage_group = self.GET_REGEX.match(result.stdout).groupdict()
        return StorageGroup(
            id=id,
            expiration_epoch=int(storage_group["expiration_epoch"]),
            group_size=int(storage_group["group_size"]),
            group_hash=None
            if storage_group["group_hash"] == "<empty>"
            else storage_group["group_hash"],
            members=[member.strip() for member in storage_group["members"].split("\n") if member],
        )

    def list(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        parse_result: bool = False,
        raw: Optional[bool] = False,
        ttl: Optional[int] = None,
        bearer: Optional[str] = None,
        lifetime: Optional[int] = None,
        address: Optional[str] = None,
        xhdr: Optional[dict] = None,
    ) -> Union[list[StorageGroup], CommandResult]:
        """
        List storage groups in NeoFS container.

        Args:
            address: Address of wallet account.
            bearer: File with signed JSON or binary encoded bearer token.
            cid: Container ID.
            parse_result: Return list of storage group objects.
            raw: Set raw request option.
            lifetime: Storage group lifetime in epochs.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header.
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        result = self._execute(
            "storagegroup list",
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "parse_result"]
            },
        )
        if not parse_result:
            return [StorageGroup(id=sg_id) for sg_id in result.stdout.strip().split("\n")]

    def delete(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        id: str,
        parse_result: bool = False,
        raw: Optional[bool] = False,
        ttl: Optional[int] = None,
        bearer: Optional[str] = None,
        lifetime: Optional[int] = None,
        address: Optional[str] = None,
        xhdr: Optional[dict] = None,
    ) -> Union[bool, CommandResult]:
        """
        Delete storage group from NeoFS.

        Args:
            address: Address of wallet account.
            bearer: File with signed JSON or binary encoded bearer token.
            cid: Container ID.
            id: Storage group identifier.
            parse_result: Return operation result.
            raw: Set raw request option.
            lifetime: Storage group lifetime in epochs.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header.
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        result = self._execute(
            "storagegroup delete",
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "parse_result"]
            },
        )
        if not parse_result:
            return result
        return result.return_code == 0
