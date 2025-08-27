from datetime import datetime, timezone
from uuid import UUID, uuid4
from msgspec import Struct, field

class Base(Struct, frozen=True, kw_only=True):
    """
    Uma classe base usada para definir propriedades comuns a comandos e eventos.

    Esta classe serve como um "contrato" inicial para outras entidades
    do sistema (como comandos ou eventos), garantindo que todas elas
    possuam um identificador único e um carimbo de tempo (timestamp).

    A biblioteca `msgspec` é utilizada em vez de `dataclasses` ou `pydantic`
    por ser extremamente rápida e otimizada para serialização e validação
    de dados (similar ao que `protobuf` ou `avro` fariam, mas em Python puro).

    Attributes
    ----------
    id : uuid.UUID
        Identificador único universal (UUID) da instância.  
        Gerado automaticamente com ``uuid4()`` se não informado.  
        Permite rastrear comandos/eventos unicamente em sistemas distribuídos.

    timestamp : datetime.datetime
        Data e hora exata da criação do objeto, em UTC.  
        Essencial para ordenação temporal, auditoria, debugging e mensageria.
    """

    id: UUID = field(default_factory=lambda: uuid4())
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))