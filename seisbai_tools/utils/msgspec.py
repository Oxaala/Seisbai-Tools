from datetime import datetime
from typing import Any, Dict, Type, TypeVar
from msgspec import json
from ulid import ULID, from_str

T = TypeVar("T")

KeyValuePair = Dict[str, Any]

def _safe_serialize(value: Any):
    """Converte tipos não nativos para representações serializáveis seguras"""
    if isinstance(value, ULID):
        return {"__type__": "ulid", "value": str(value)}
    elif isinstance(value, datetime):
        return {"__type__": "datetime", "value": value.isoformat()}
    elif isinstance(value, (int, float, str, bool, type(None))):
        return value
    else:
        return {"__type__": "repr", "value": repr(value)}

def struct_to_dict(element: Any):
    """Cria dict serializável da instância (funciona com msgspec.Struct)"""
    fields = getattr(element, "__struct_fields__", [])
    return {k: _safe_serialize(getattr(element, k)) for k in fields}

def _safe_deserialize(value: KeyValuePair) -> Any:
    """Converte representações serializadas de volta para objetos reais"""
    if "__type__" in value:
        type_name = value["__type__"]
        val = value["value"]

        if type_name == "ulid":
            return from_str(val)
        elif type_name == "datetime":
            return datetime.fromisoformat(val)
        elif type_name == "repr":
            return val
        else:
            return value
    elif isinstance(value, list):
        return [_safe_deserialize(v) for v in value]
    else:
        return value

def dict_to_struct(data: Dict[str, Any]) -> Dict[str, Any]:
    """Restaura campos serializados via _safe_deserialize"""
    return {k: _safe_deserialize(v) for k, v in data.items()}

def serialize_to_json(data: Any):
    return json.encode(data).decode()

def serialize_to_bytes(data: Any):
    return json.encode(data)

def deserialize(data: bytes, type: Type[T]) -> T:
    return json.decode(data, type=type)