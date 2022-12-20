from dataclasses import dataclass


@dataclass
class Blobstor:
    path: str
    path_type: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise RuntimeError(f"Only two {self.__class__.__name__} instances can be compared")
        return self.path == other.path and self.path_type == other.path_type

    def __hash__(self):
        return hash((self.path, self.path_type))

@dataclass
class Shard:
    blobstor: list[Blobstor]
    metabase: str
    writecache: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise RuntimeError(f"Only two {self.__class__.__name__} instances can be compared")
        return (
            set(self.blobstor) == set(other.blobstor)
            and self.metabase == other.metabase
            and self.writecache == other.writecache
        )

    def __hash__(self):
        return hash((self.metabase, self.writecache))
