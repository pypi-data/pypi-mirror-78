import contextlib
import json
import os

from . import dotenv


class _Empty:
    def __str__(self):
        return "EMPTY"


empty = _Empty()


class Env:

    @classmethod
    def load(cls, strict=True, **kwargs):
        data = dotenv.read_dotenv(dotenv.find_dotenv(**kwargs))
        if data is None and strict:
            raise FileNotFoundError("dotenv file not found.")
        return cls(data or ())

    def __init__(self, __updates=(), **updates):
        # update parameters to os.environ, only if they are not set
        dict(__updates, **updates).items()
        env = {
            k: v for k, v in dict(__updates, **updates).items()
            if k not in os.environ
        }
        os.environ.update(env)

    def read(self, key, cast, *, default=empty):  # noqa
        with contextlib.suppress(KeyError):
            return cast(os.environ[key])
        if default is not empty:
            return default
        raise LookupError(
            f"Could not find {key!r} in environment, "
            f"and default was not provided"
        )

    def str(self, key, *, default=empty):
        return self.read(key, cast=str, default=default)

    def bool(self, key, *, default=empty):
        return self.read(key, cast=lambda v: v.lower() == "true", default=default)

    def int(self, key, *, default=empty):
        return self.read(key, cast=int, default=default)

    def float(self, key, *, default=empty):
        return self.read(key, cast=float, default=default)

    def json(self, key, *, default=empty):
        return self.read(key, cast=json.loads, default=default)

    def list(self, key, *, default=empty):
        return self.read(key, cast=lambda v: [i.strip() for i in v.split(",")], default=default)

    def tuple(self, key, *, default=empty):
        return self.read(key, lambda v: tuple(i.strip() for i in v.lstrip("(").rstrip(")").split(",")), default=default)

    def dict(self, key, *, default=empty):
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
