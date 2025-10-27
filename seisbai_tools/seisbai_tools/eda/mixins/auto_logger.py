from datetime import datetime
import os
import socket
from threading import Lock
from typing import Any, Dict

from msgspec import json
from ...pub_sub import PubSub
from ...utils.get_log_dir import get_default_log_dir
from ulid import ULID

_file_locks: Dict[str, Lock] = {}

def _safe_serialize(value: Any):
    """Converte tipos não nativos para string"""
    if isinstance(value, ULID):
        return str(value)
    elif isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, (int, float, str, bool, type(None))):
        return value
    else:
        return repr(value)

def _to_dict(element: Any):
    """Cria dict serializável da instância (funciona com msgspec.Struct)"""
    fields = getattr(element, "__struct_fields__", [])
    return {k: _safe_serialize(getattr(element, k)) for k in fields}

def _write_log(file_path: str, entry: Dict[str, Any]):
    if file_path not in _file_locks:
        _file_locks[file_path] = Lock()
    
    lock = _file_locks[file_path]

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with lock:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.encode(entry).decode("utf-8") + "\n")

class AutoLoggerMixin:
    def __post_init__(self):
        print("Logar")
        super_post_init = getattr(super, "__post_init__", None)

        if callable(super_post_init):
            super_post_init()
        
        log_dir = getattr(self, "log_dir", get_default_log_dir())
        hostname = socket.gethostname()
        session = PubSub().session()
        log_file = os.path.join(log_dir, f"{session}_{hostname}.log")

        entry = {
            "timestamp": getattr(self, "timestamp").isoformat(),
            "id": str(getattr(self, "id", None)),
            "name": self.__class__.__name__,
            "data": _to_dict(self)
        }

        _write_log(log_file, entry)