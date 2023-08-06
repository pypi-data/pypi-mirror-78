__all__ = ["MultiCache", "Cache"]


import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from textwrap import indent
from typing import Any, Dict, Optional

from .common import dump_json, load_json
from .utils import FileSystemPath, format_directory


class Cache:
    """An expiring filesystem cache that can store serialized json."""

    INDEX_FILE = "index.json"

    def __init__(self, directory: FileSystemPath):
        self.deleted = False
        self.directory = Path(directory).resolve()
        self.index_path = self.directory / self.INDEX_FILE
        self.index = (
            load_json(self.index_path)
            if self.index_path.is_file()
            else self.get_initial_index()
        )
        self.flush()

    def get_initial_index(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "expires": None,
            "json": {},
        }

    @property
    def json(self) -> Dict[str, Any]:
        return self.index["json"]

    @property
    def expires(self) -> Optional[datetime]:
        expires = self.index["expires"]
        return expires and datetime.fromisoformat(expires)

    @expires.setter
    def expires(self, value: Optional[datetime]):
        self.index["expires"] = value and value.isoformat()

    def timeout(self, delta: timedelta = None, **kwargs):
        if not delta:
            delta = timedelta()
        delta += timedelta(**kwargs)
        self.expires = datetime.fromisoformat(self.index["timestamp"]) + delta

    def restart_timeout(self):
        now = datetime.now()
        timestamp = datetime.fromisoformat(self.index["timestamp"])

        if self.expires:
            self.expires += now - timestamp

        self.index["timestamp"] = now.isoformat()

    def __enter__(self) -> "Cache":
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.flush()

    def delete(self):
        if not self.deleted:
            if self.directory.is_dir():
                shutil.rmtree(self.directory)
            self.index = self.get_initial_index()
            self.deleted = True

    def clear(self):
        self.delete()
        self.deleted = False
        self.flush()

    def flush(self):
        if self.deleted:
            return

        if self.expires and self.expires <= datetime.now():
            self.clear()
        else:
            self.directory.mkdir(parents=True, exist_ok=True)
            dump_json(self.index, self.index_path)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self.directory)!r})"

    def __str__(self) -> str:
        formatted_json = indent(json.dumps(self.json, indent=2), "  │  ")[5:]
        contents = indent("\n".join(format_directory(self.directory)), "  │    ")

        return (
            f"Cache {self.index_path.parent.name}:\n"
            f"  │  timestamp = {datetime.fromisoformat(self.index['timestamp']).ctime()}\n"
            f"  │  expires = {self.expires and self.expires.ctime()}\n  │  \n"
            f"  │  directory = {self.directory}\n{contents}\n  │  \n"
            f"  │  json = {formatted_json}"
        )


class MultiCache(Dict[str, Cache]):
    """A container of lazily instantiated named caches."""

    DEFAULT_CACHE = "default"

    def __init__(self, directory: FileSystemPath):
        self.path = Path(directory).resolve()

    def __missing__(self, key: str) -> Cache:
        cache = Cache(self.path / key)
        self[key] = cache
        return cache

    def __delitem__(self, key: str):
        self[key].delete()
        super().__delitem__(key)

    @property
    def directory(self) -> Path:
        return self[self.DEFAULT_CACHE].directory

    @property
    def json(self) -> Dict[str, Any]:
        return self[self.DEFAULT_CACHE].json

    def __enter__(self) -> "MultiCache":
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.flush()

    def preload(self):
        if not self.path.is_dir():
            return
        for directory in self.path.iterdir():
            if (directory / Cache.INDEX_FILE).is_file():
                self[directory.name]

    def clear(self):
        if self.path.is_dir():
            shutil.rmtree(self.path)
        super().clear()

    def flush(self):
        for cache in self.values():
            cache.flush()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self.path)!r})"
