__all__ = ["Env"]

import json
import os
from contextlib import suppress
from typing import Callable, Dict, List, Tuple, TypeVar, Union

empty = type("Empty", (), dict(__str__=lambda s: "EMPTY"))
T = TypeVar("T")
D = TypeVar("D")


class Env:
    def __init__(self, env: Dict = None, **updates):
        # update parameters to os.environ, only if they are not set
        env = {
            k: v for k, v in dict(env or {}, **updates).items()
            if k not in os.environ
        }
        os.environ.update(env)

    def read(self, key: str, cast: Callable[[str], T], *, default: D = empty) -> Union[T, D]:  # noqa
        with suppress(KeyError):
            return cast(os.environ[key])
        if default is empty:
            raise LookupError(f"Could not find {key} in environment, and default was not provided")
        return default

    def str(self, key: str, *, default: D = empty) -> Union[str, D]:
        return self.read(key, cast=str, default=default)

    def bool(self, key: str, *, default: D = empty) -> Union[bool, D]:
        return self.read(key, cast=lambda v: v.lower() == "true", default=default)

    def int(self, key: str, *, default: D = empty) -> Union[int, D]:
        return self.read(key, cast=int, default=default)

    def float(self, key: str, *, default: D = empty) -> Union[float, D]:
        return self.read(key, cast=float, default=default)

    def json(self, key: str, *, default: D = empty) -> Union[str, bool, int, float, None, list, dict, D]:
        return self.read(key, cast=json.loads, default=default)

    def list(self, key: str, *, default: D = empty) -> Union[List[str], D]:
        return self.read(key, cast=lambda v: [i.strip() for i in v.split(",")], default=default)

    def tuple(self, key: str, *, default: D = empty) -> Union[Tuple[str], D]:
        return self.read(key, lambda v: tuple(i.strip() for i in v.lstrip("(").rstrip(")").split(",")), default=default)

    def dict(self, key: str, *, default: D = empty) -> Union[Dict[str, str], D]:
        return self.read(
            key,
            cast=lambda v: {
                k: v for k, v in (
                    p.strip().partition("=")[::2]
                    for p in v.split(";") if p.strip()
                )
            },
            default=default
        )
