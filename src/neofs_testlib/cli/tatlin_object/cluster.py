from neofs_testlib.cli.cli_command import CliCommand
from neofs_testlib.shell import CommandResult


class TatlinObjectCllCluster(CliCommand):
    def init(
        self,
        cluster: str,
        size: int,
    ) -> CommandResult:
        """
        Cluster initialization

        Args:
            cluster: Unique cluster name, Example: --cluster yadro.cluster.
            size: Cluster size. Only 4 or 8 nodes.

        Returns:
            Command's result.
        """
        return self._execute(
            "cluster init",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def join(
        self,
        cluster: str,
        peer: str,
    ) -> CommandResult:
        """
        Node join into bootstrap processing.

        Args:
            cluster: Unique cluster name, Example: --cluster yadro.cluster.
            peer: <node ip> of node where Init was performed.

        Returns:
            Command's result.
        """

        return self._execute(
            "cluster join",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def get_version(self) -> str:
        """
        Get cluster version.

        Returns:
            Cluster version.
        """

        result = self._execute(
            "cluster version get",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )
        return "".join(result.stdout).split("VERSION=")[1].strip("\"")
