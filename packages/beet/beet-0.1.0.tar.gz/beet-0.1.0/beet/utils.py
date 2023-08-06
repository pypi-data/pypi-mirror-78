__all__ = [
    "FileSystemPath",
    "ensure_optional_value",
    "extra_field",
    "import_from_string",
    "format_exc",
    "format_obj",
    "format_directory",
    "list_files",
]


import os
from dataclasses import field
from importlib import import_module
from pathlib import Path
from traceback import format_exception
from typing import Optional, Union, TypeVar, Any, Iterator


FileSystemPath = Union[str, os.PathLike]


T = TypeVar("T")


def ensure_optional_value(arg: Optional[T]) -> T:
    assert arg is not None
    return arg


def extra_field(**kwargs) -> Any:
    return field(repr=False, hash=False, compare=False, **kwargs)


def import_from_string(dotted_path: str, default_member: str = None) -> Any:
    try:
        module = import_module(dotted_path)
    except ImportError:
        if "." not in dotted_path:
            raise

        dotted_path, _, default_member = dotted_path.rpartition(".")

        try:
            module = import_module(dotted_path)
        except Exception as exc:
            raise exc from None

    return getattr(module, default_member) if default_member else module


def format_exc(exc: BaseException) -> str:
    return "".join(format_exception(exc.__class__, exc, exc.__traceback__))


def format_obj(obj: Any) -> str:
    module = getattr(obj, "__module__", None)
    name = getattr(obj, "__qualname__", None)
    return repr(f"{module}.{name}") if module and name else repr(obj)


def format_directory(directory: FileSystemPath, prefix: str = "") -> Iterator[str]:
    entries = list(sorted(Path(directory).iterdir()))
    indents = ["├─"] * (len(entries) - 1) + ["└─"]

    for indent, entry in zip(indents, entries):
        yield f"{prefix}{indent} {entry.name}"

        if entry.is_dir():
            indent = "│  " if indent == "├─" else "   "
            yield from format_directory(entry, prefix + indent)


def list_files(directory: FileSystemPath) -> Iterator[Path]:
    for root, _, files in os.walk(directory):
        for filename in files:
            yield Path(root, filename).relative_to(directory)
