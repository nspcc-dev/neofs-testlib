from dataclasses import dataclass
from typing import Optional


@dataclass
class StorageObject:
    cid: Optional[str] = None
    oid: Optional[str] = None
    owner: Optional[str] = None

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise RuntimeError(f"Only two {self.__class__.__name__} instances can be compared")
        return self.oid == other.oid and self.cid == other.cid

    def __hash__(self):
        return hash((self.cid, self.oid))
