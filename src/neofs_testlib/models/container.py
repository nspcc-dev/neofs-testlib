from dataclasses import dataclass
from typing import Optional


@dataclass
class Container:
    cid: Optional[str] = None
    name: Optional[str] = None
    owner: Optional[str] = None
    basic_acl: Optional[str] = None
    created: Optional[str] = None
    attributes: Optional[dict[str, str]] = None
    placement_policy: Optional[str] = None

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise RuntimeError(f"Only two {self.__class__.__name__} instances can be compared")
        return self.cid == other.cid

    def __hash__(self):
        return hash((self.cid, ))
