from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union
)

class _Empty: ...
empty: _Empty

_T = TypeVar("_T")
_D = TypeVar("_D")

_C = Callable[[str], _T]
_JSBase = Union[str, bool, int, float, None, List, Dict]
_JS = Union[
    _JSBase,
    List[_JSBase],
    Dict[str, _JSBase]
]
_Seq = Union[
    Mapping[str, str],
    Iterable[Tuple[str, str]]
]


class Env:
    @classmethod
    def load(
        cls: Type[_T],
        strict: bool=..., *,
        variable: Optional[str]=...,
        filename: str=...,
        path: str=...,
        find: bool=...
    ) -> _T: ...
    def __init__(self, __updates: _Seq=..., **updates: str): ...
    def read(self, key: str, cast: _C, *, default: _D=...) -> Union[_D, _T]: ...
    def tuple(self, key: str, *, default: _D=...) -> Union[_D, Tuple[str, ...]]: ...
    def float(self, key: str, *, default: _D=...) -> Union[_D, float]: ...
    def bool(self, key: str, *, default: _D=...) -> Union[_D, bool]: ...
    def json(self, key: str, *, default: _D=...) -> Union[_D, _JS]: ...
    def list(self, key: str, *, default: _D=...) -> Union[_D, List[str]]: ...
    def dict(self, key: str, *, default: _D=...) -> Union[_D, Dict[str, str]]: ...
    def int(self, key: str, *, default: _D=...) -> Union[_D, int]: ...
    def str(self, key: str, *, default: _D=...) -> Union[_D, str]: ...
