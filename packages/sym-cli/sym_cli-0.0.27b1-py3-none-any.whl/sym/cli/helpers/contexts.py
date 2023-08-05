from contextlib import contextmanager
from os import environ
from typing import Iterator, Optional

EnvValue = Optional[str]


def _set_env(key: str, value: EnvValue) -> EnvValue:
    last: EnvValue
    try:
        last = environ[key]
    except KeyError:
        last = None

    if value is not None:
        environ[key] = value
    elif last is not None:
        del environ[key]
    return last


@contextmanager
def push_env(key: str, value: EnvValue) -> Iterator[EnvValue]:
    saved = _set_env(key, value)

    try:
        yield saved
    finally:
        _set_env(key, saved)
