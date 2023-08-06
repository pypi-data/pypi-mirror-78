import importlib
from collections.abc import Sequence
from pathlib import Path


def import_all(filename, name):
    for path in Path(filename).resolve().parent.glob("*.py"):
        if path.stem != "__init__":
            importlib.import_module(f".{path.stem}", name)


def wrap(val):
    if isinstance(val, Sequence):
        return val
    else:
        return (val,)
