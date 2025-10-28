from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID, uuid4
from msgspec import Struct, field
from ..utils.msgspec import dict_to_struct, struct_to_dict

from ..utils.get_class_type import get_type
from ..utils.import_path import get_import_path


class _Payload(Struct):
    type_path: str
    data: Dict[str, Any]

    @classmethod
    def from_object(cls, obj: object) -> "_Payload":
        """Cria payload a partir de um objeto comum"""
        return cls(type_path=get_import_path(type(obj)), data=struct_to_dict(obj))

    def reconstruct(self) -> Any:
        """Reconstrói o objeto original"""
        cls = get_type(self.type_path)
        return cls(**dict_to_struct(self.data))


class Package(Struct):
    payload: _Payload
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    @classmethod
    def wrap(cls, obj: object) -> "Package":
        return cls(payload=_Payload.from_object(obj))