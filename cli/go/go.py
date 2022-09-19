from typing import Optional

from shell import Shell

from .candidate import NeoGoCandidate
from .contract import NeoGoContract
from .db import NeoGoDb
from .nep17 import NeoGoNep17
from .node import NeoGoNode
from .query import NeoGoQuery
from .version import NeoGoVersion
from .wallet import NeoGoWallet


class NeoGo:
    neo_go_exec_path: Optional[str] = None
    config_path: Optional[str] = None
    candidate: Optional[NeoGoCandidate] = None
    contract: Optional[NeoGoContract] = None
    db: Optional[NeoGoDb] = None
    nep17: Optional[NeoGoNep17] = None
    node: Optional[NeoGoNode] = None
    query: Optional[NeoGoQuery] = None
    version: Optional[NeoGoVersion] = None
    wallet: Optional[NeoGoWallet] = None

    def __init__(
        self,
        shell: Shell,
        neo_go_exec_path: Optional[str] = None,
        config_path: Optional[str] = None,
    ):
        self.candidate = NeoGoCandidate(
            shell, neo_go_exec_path, config_path=config_path
        )
        self.contract = NeoGoContract(
            self.neo_go_exec_path, config_path=config_path
        )
        self.db = NeoGoDb(shell, neo_go_exec_path, config_path=config_path)
        self.nep17 = NeoGoNep17(shell, neo_go_exec_path, config_path=config_path)
        self.node = NeoGoNode(shell, neo_go_exec_path, config_path=config_path)
        self.query = NeoGoQuery(shell, neo_go_exec_path, config_path=config_path)
        self.version = NeoGoVersion(shell, neo_go_exec_path, config_path=config_path)
        self.wallet = NeoGoWallet(shell, neo_go_exec_path, config_path=config_path)
