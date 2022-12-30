from typing import Optional

from neofs_testlib.cli.tatlin_object.cluster import TatlinObjectCllCluster
from neofs_testlib.shell import Shell


class TatlinObjectCli:
    cluster: Optional[TatlinObjectCllCluster] = None

    def __init__(self, shell: Shell, neofs_cli_exec_path: str):
        self.cluster = TatlinObjectCllCluster(shell, neofs_cli_exec_path)
