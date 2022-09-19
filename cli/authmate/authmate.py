from typing import Optional

from shell import Shell

from .secret import NeofsAuthmateSecret
from .version import NeofsAuthmateVersion


class NeofsAuthmate:
    secret: Optional[NeofsAuthmateSecret] = None
    version: Optional[NeofsAuthmateVersion] = None

    def __init__(
        self,
        shell: Shell,
        neofs_authmate_exec_path: str,
    ):

        self.secret = NeofsAuthmateSecret(shell, neofs_authmate_exec_path)
        self.version = NeofsAuthmateVersion(shell, neofs_authmate_exec_path)
