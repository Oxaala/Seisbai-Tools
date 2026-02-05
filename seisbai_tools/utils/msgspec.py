from datetime import datetime
from uuid import UUID
from typing import Any
import msgspec
import importlib
from ulid import ULID, from_str

def serialize(obj: Any) -> bytes:
    def convert(o):
        # Tipos especiais
        if isinstance(o, ULID):
            return {"__type__": "ULID", "value": str(o)}
        if isinstance(o, UUID):
            return {"__type__": "UUID", "value": str(o)}
        if isinstance(o, datetime):
            return {"__type__": "datetime", "value": o.isoformat()}
        
        # numpy arrays - converter para lista
        try:
            import numpy as np
            if isinstance(o, np.ndarray):
                return {"__type__": "numpy.ndarray", "value": o.tolist(), "shape": list(o.shape), "dtype": str(o.dtype)}
        except ImportError:
            pass

        # msgspec.Struct
        if isinstance(o, msgspec.Struct):
            data = {field: convert(getattr(o, field)) for field in o.__struct_fields__}
            data["__class_path__"] = f"{o.__class__.__module__}.{o.__class__.__name__}"
            return data

        # listas
        if isinstance(o, list):
            return [convert(i) for i in o]

        # dicts
        if isinstance(o, dict):
            return {k: convert(v) for k, v in o.items()}

        # primitivos
        return o

    return msgspec.json.encode(convert(obj))


# --- Desserialização automática ---
def deserialize(data: bytes) -> Any:
    obj = msgspec.json.decode(data)

    def restore(o):
        if isinstance(o, dict):
            # Tipos especiais
            if "__type__" in o:
                t = o["__type__"]
                if t == "ULID":
                    return from_str(o["value"])
                if t == "UUID":
                    return UUID(o["value"])
                if t == "datetime":
                    return datetime.fromisoformat(o["value"])

            # Instância de msgspec.Struct
            cls_path = o.get("__class_path__")
            if cls_path:
                module_name, class_name = cls_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                cls = getattr(module, class_name)
                data = {k: restore(v) for k, v in o.items() if k != "__class_path__"}
                return cls(**data)

            # dict normal
            return {k: restore(v) for k, v in o.items()}

        elif isinstance(o, list):
            return [restore(i) for i in o]

        return o

    return restore(obj)