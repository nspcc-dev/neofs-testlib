from dataclasses import dataclass
from typing import Optional


@dataclass
class Eacl:
    eacl: Optional[str] = None
    signature: Optional[str] = None

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise RuntimeError(f"Only two {self.__class__.__name__} instances can be compared")
        return self.eacl == other.eacl

    def __hash__(self):
        return hash((self.eacl, ))
