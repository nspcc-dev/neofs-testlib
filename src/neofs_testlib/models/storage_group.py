from dataclasses import dataclass
from typing import Optional


@dataclass
class StorageGroup:
    id: Optional[str] = None
    expiration_epoch: Optional[int] = None
    group_size: Optional[int] = None
    group_hash: Optional[str] = None
    members: Optional[list[str]] = None

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise RuntimeError(f"Only two {self.__class__.__name__} instances can be compared")
        return self.id == other.id

    def __hash__(self):
        return hash((self.id, ))
