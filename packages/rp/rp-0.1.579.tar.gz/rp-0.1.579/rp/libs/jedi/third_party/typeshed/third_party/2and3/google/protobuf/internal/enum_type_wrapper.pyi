from typing import Any, List, Tuple

class EnumTypeWrapper(object):
    def __init__(self, enum_type: Any) -> None: ...
    def Name(self, number: int) -> bytes: ...
    def Value(self, name: bytes) -> int: ...
    def keys(self) -> List[bytes]: ...
    def values(self) -> List[int]: ...

    @classmethod
    def items(cls) -> List[Tuple[bytes, int]]: ...
