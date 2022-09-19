from typing import Optional

from shell import Shell

from .config import NeofsAdmConfig
from .morph import NeofsAdmMorph
from .subnet import NeofsAdmMorphSubnet
from .storage_config import NeofsAdmStorageConfig
from .version import NeofsAdmVersion


class NeofsAdm:
    config: Optional[NeofsAdmConfig] = None
    morph: Optional[NeofsAdmMorph] = None
    subnet: Optional[NeofsAdmMorphSubnet] = None
    storage_config: Optional[NeofsAdmStorageConfig] = None
    version: Optional[NeofsAdmVersion] = None

    def __init__(self, shell: Shell, neofs_adm_exec_path: str, config_file: Optional[str] = None):
        self.config = NeofsAdmConfig(shell, neofs_adm_exec_path, config=config_file)
        self.morph = NeofsAdmMorph(shell, neofs_adm_exec_path, config=config_file)
        self.subnet = NeofsAdmMorphSubnet(shell, neofs_adm_exec_path, config=config_file)
        self.storage_config = NeofsAdmStorageConfig(shell, neofs_adm_exec_path, config=config_file)
        self.version = NeofsAdmVersion(shell, neofs_adm_exec_path, config=config_file)
