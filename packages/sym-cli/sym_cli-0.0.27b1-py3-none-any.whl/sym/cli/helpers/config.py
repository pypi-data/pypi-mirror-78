import hashlib
import json
import os
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import (
    Any,
    Final,
    Iterator,
    Literal,
    MutableMapping,
    Optional,
    TypedDict,
    cast,
)

import immutables
import yaml
from portalocker.exceptions import AlreadyLocked

from .io import TruncatingStringIO
from .os import create_lock, read_lock, read_write_lock

ConfigKey = Literal["org", "email"]


def xdg_config_home() -> Path:
    try:
        return Path(os.environ["XDG_CONFIG_HOME"])
    except KeyError:
        return Path.home() / ".config"


def sym_config_file(file_name: str) -> Path:
    sym_config_home = xdg_config_home() / "sym"
    return sym_config_home / file_name


class SymConfigFile:
    def __init__(self, *, file_name: str, **dependencies):
        path = Path()
        if dependencies:
            key = json.dumps(dependencies, sort_keys=True).encode("utf-8")
            md5 = hashlib.md5(key).hexdigest()
            path = path / md5
        self.path = sym_config_file(path / file_name)

        self.read_lock = read_lock(self.path)
        self.write_lock = create_lock(self.path)
        self.update_lock = read_write_lock(self.path)

    def __enter__(self):
        self.mkparents()
        try:
            # acquire read lock, hold across context
            fh = self.read_lock.acquire()
            fh.seek(0)  # reentrant
            self.value = fh.read()
        except FileNotFoundError:
            self.value = None
        self.file = TruncatingStringIO(initial_value=self.value)
        return self.file

    def __exit__(self, type, value, traceback):
        self.read_lock.release()  # release read lock
        if value:
            return
        if self.file.tell() == 0:
            return
        if self.value != (value := self.file.getvalue()):
            with self.exclusive_access() as f:
                f.write(value)

    def __str__(self):
        return str(self.path)

    def mkparents(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def put(self, s: str):
        with self as f:
            f.write(s)

    def _throwaway_write(self):
        with NamedTemporaryFile(mode="w+") as f:
            yield f

    @contextmanager
    def exclusive_access(self):
        try:
            with self.write_lock as f:  # acquire write lock
                yield f
        except AlreadyLocked:  # another thread is writing same value
            yield from self._throwaway_write()

    @contextmanager
    def exclusive_create(self):
        self.mkparents()
        if self.path.exists():
            yield from self._throwaway_write()
        else:
            with self.exclusive_access() as f:
                yield f

    @contextmanager
    def update(self):
        self.mkparents()
        with self.update_lock as f:
            f.seek(0)  # reentrant
            yield f


class ServerConfigSchema(TypedDict):
    last_connection: datetime


class ConfigSchema(TypedDict, total=False):
    org: str
    email: str
    default_resource: str
    servers: MutableMapping[str, ServerConfigSchema]


class Config(MutableMapping[ConfigKey, Any]):
    __slots__ = ["file", "config"]

    file: Final[SymConfigFile]
    config: Final[ConfigSchema]

    def __init__(self) -> None:
        self.file = SymConfigFile(file_name="config.yml")
        with self.file as f:
            self.__load(f)

    def __load(self, fh):
        self.config = cast(ConfigSchema, yaml.safe_load(stream=fh) or {})

    def __flush(self, fh) -> None:
        fh.seek(0)
        fh.truncate()
        yaml.safe_dump(self.config, stream=fh)

    def __getitem__(self, key: ConfigKey) -> Any:
        item = self.config[key]
        if isinstance(item, dict):
            return immutables.Map(item)
        return item

    def __delitem__(self, key: ConfigKey) -> None:
        with self.atomic() as f:
            del self.config[key]
            self.__flush(f)

    def __setitem__(self, key: ConfigKey, value: Any) -> None:
        with self.atomic() as f:
            if isinstance(value, immutables.Map):
                value = dict(value)
            self.config[key] = value
            self.__flush(f)

    def __iter__(self) -> Iterator[ConfigKey]:
        return cast(Iterator[ConfigKey], iter(self.config))

    def __len__(self) -> int:
        return len(self.config)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({str(self.file)})"

    @contextmanager
    def atomic(self):
        with self.file.update() as f:
            self.__load(f)
            yield f

    @classmethod
    def reset(cls):
        setattr(cls, "__instance", cls())

    @classmethod
    def instance(cls) -> "Config":
        if not hasattr(cls, "__instance"):
            cls.reset()
        return getattr(cls, "__instance")

    @classmethod
    def get_default(cls, key) -> Optional[str]:
        return cls.instance().get(f"default_{key}")

    @classmethod
    def get_org(cls) -> str:
        return cls.instance()["org"]

    @classmethod
    def get_email(cls) -> str:
        return cls.instance()["email"]

    @classmethod
    def get_servers(cls) -> str:
        return cls.instance().get("servers", immutables.Map())

    @classmethod
    def get_instance(cls, instance: str) -> str:
        return cls.get_servers().get(instance, ServerConfigSchema())

    @classmethod
    def touch_instance(cls, instance: str, error: bool = False):
        with cls.instance().atomic():
            instance_config = cls.get_instance(instance)
            instance_config["last_connection"] = None if error else datetime.now()
            cls.instance()["servers"] = cls.get_servers().set(instance, instance_config)
