import re
from typing import Optional, Union

from neofs_testlib.cli.cli_command import CliCommand
from neofs_testlib.shell import CommandResult
from neofs_testlib.models import Container, Eacl, StorageObject


class NeofsCliContainer(CliCommand):
    CID_REGEX = re.compile(r"container ID: (\w+)")
    GET_REGEX = re.compile(
        r"container ID: (?P<cid>\w+)\n"
        r"owner ID: (?P<owner>\w+)\n"
        r"basic ACL: (?P<basic_acl>\w{8}).+\n"
        r"((.*\n){4})?"
        r"created: (?P<created>.+)\n"
        r"attributes:\n"
        r"(?P<attributes>(\t.*\n)*)"
        r"placement policy:\n"
        r"(?P<placement_policy>(.*\n)+)"
    )
    EACL_REGEX = re.compile(r"eACL: \n" r"(?P<eacl>(.*\n)+)" r"(Signature: (?P<signature>.+)\n)?")

    def create(
        self,
        rpc_endpoint: str,
        wallet: str,
        address: Optional[str] = None,
        attributes: Optional[dict] = None,
        basic_acl: Optional[str] = None,
        await_mode: bool = False,
        disable_timestamp: bool = False,
        parse_result: bool = False,
        name: Optional[str] = None,
        nonce: Optional[str] = None,
        policy: Optional[str] = None,
        session: Optional[str] = None,
        subnet: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
    ) -> Union[Container, CommandResult]:
        """
        Create a new container and register it in the NeoFS.
        It will be stored in the sidechain when the Inner Ring accepts it.

        Args:
            address: Address of wallet account.
            attributes: Comma separated pairs of container attributes in form of
                Key1=Value1,Key2=Value2.
            await_mode: Block execution until container is persisted.
            basic_acl: Hex encoded basic ACL value or keywords like 'public-read-write',
                'private', 'eacl-public-read' (default "private").
            disable_timestamp: Disable timestamp container attribute.
            name: Container name attribute.
            nonce: UUIDv4 nonce value for container.
            parse_result: Return Container object
            policy: QL-encoded or JSON-encoded placement policy or path to file with it.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            session: Path to a JSON-encoded container session token.
            subnet: String representation of container subnetwork.
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Created container.
        """
        result = self._execute(
            "container create",
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "parse_result"]
            },
        )
        if not parse_result:
            return result
        cids = self.CID_REGEX.findall(result.stdout)
        assert len(cids) == 1
        return Container(cid=cids[0])

    def delete(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        address: Optional[str] = None,
        await_mode: bool = False,
        parse_result: bool = False,
        session: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
        force: bool = False,
    ) -> Union[CommandResult, bool]:
        """
        Delete an existing container.
        Only the owner of the container has permission to remove the container.

        Args:
            address: Address of wallet account.
            await_mode: Block execution until container is removed.
            cid: Container ID.
            force: Do not check whether container contains locks and remove immediately.
            parse_result: Return operation result.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            session: Path to a JSON-encoded container session token.
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """

        result = self._execute(
            "container delete",
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "parse_result"]
            },
        )
        if not parse_result:
            return result
        return result.return_code == 0

    def get(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        address: Optional[str] = None,
        await_mode: bool = False,
        parse_result=False,
        to: Optional[str] = None,
        json_mode: bool = False,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
    ) -> Union[Container, CommandResult]:
        """
        Get container field info.

        Args:
            address: Address of wallet account.
            await_mode: Block execution until container is removed.
            cid: Container ID.
            json_mode: Print or dump container in JSON format.
            parse_result: Return Container object.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            to: Path to dump encoded container.
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        assert not parse_result * json_mode, "Parse json response not supported"
        result = self._execute(
            "container get",
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "parse_result"]
            },
        )
        if not parse_result:
            return result
        container = self.GET_REGEX.match(result.stdout).groupdict()
        attributes = dict(
            {
                tuple(attribute.strip().split("=", 1))
                for attribute in container["attributes"].strip().split("\n")
                if attribute
            }
        )
        return Container(
            cid=container["cid"],
            owner=container["owner"],
            created=container["created"],
            name=attributes["Name"] if attributes["Name"] else None,
            attributes=attributes,
            basic_acl=container["basic_acl"],
            placement_policy=container["placement_policy"].replace("\n", " ").strip(),
        )

    def get_eacl(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        parse_result: bool = False,
        address: Optional[str] = None,
        await_mode: bool = False,
        to: Optional[str] = None,
        session: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
    ) -> Union[Eacl, CommandResult]:
        """
        Get extended ACL table of container.

        Args:
            address: Address of wallet account.
            await_mode: Block execution until container is removed.
            cid: Container ID.
            parse_result: Return eACL object
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            to: Path to dump encoded container.
            session: Path to a JSON-encoded container session token.
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.

        """
        result = self._execute(
            "container get-eacl",
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "parse_result"]
            },
        )
        if not parse_result:
            return result
        eacl = self.EACL_REGEX.match(result.stdout).groupdict()
        return Eacl(
            eacl=eacl["eacl"],
            signature=eacl["signature"],
        )

    def list_objects(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        parse_result: bool = False,
        address: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
    ) -> Union[list[StorageObject], CommandResult]:
        """
        List existing objects in container.

        Args:
            address: Address of wallet account.
            cid: Container ID.
            parse_result: Return list of object.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        result = self._execute(
            "container list-objects",
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "parse_result"]
            },
        )
        if not parse_result:
            return result
        return [StorageObject(cid=cid, oid=oid) for oid in result.stdout.strip().split("\n")]

    def list(
        self,
        rpc_endpoint: str,
        wallet: str,
        address: Optional[str] = None,
        owner: Optional[str] = None,
        parse_result: bool = False,
        get_full_info: bool = False,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
        **params,
    ) -> Union[list[Container], CommandResult]:
        """
        List all created containers.

        Args:
            address: Address of wallet account.
            owner: Owner of containers (omit to use owner from private key).
            parse_result: Return list of containers object.
            get_full_info: Return list of containers object with full info (slowly).
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        query_params = {
            param: value
            for param, value in locals().items()
            if param not in ["self", "parse_result", "get_full_info"]
        }
        result = self._execute("container list", **query_params)
        if not parse_result:
            return result

        return (
            [
                self.get(cid=cid, **query_params, parse_result=True)
                for cid in result.stdout.strip().split("\n")
            ]
            if get_full_info
            else [Container(cid=cid) for cid in result.stdout.strip().split("\n")]
        )

    def set_eacl(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        parse_result: bool = False,
        address: Optional[str] = None,
        await_mode: bool = False,
        table: Optional[str] = None,
        session: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
    ) -> Union[bool, CommandResult]:
        """
        Set a new extended ACL table for the container.
        Container ID in the EACL table will be substituted with the ID from the CLI.

        Args:
            address: Address of wallet account.
            await_mode: Block execution until container is removed.
            cid: Container ID.
            parse_result: Return operation result
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            session: Path to a JSON-encoded container session token.
            table: Path to file with JSON or binary encoded EACL table.
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        result = self._execute(
            "container set-eacl",
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "parse_result"]
            },
        )
        if not parse_result:
            return result
        return result.return_code == 0
