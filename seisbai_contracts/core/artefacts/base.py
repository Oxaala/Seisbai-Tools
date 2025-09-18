from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4
from msgspec import Struct, field

class Base(Struct, frozen=True, kw_only=True):
    """
    Uma classe base imutável para definir propriedades comuns a comandos e eventos.

    Esta classe atua como um contrato para entidades do sistema 
    (como comandos ou eventos), garantindo que todas possuam:
    - um identificador único,
    - um carimbo de tempo (timestamp),
    - uma mensagem descritiva,
    - e opcionalmente um identificador de conexão associado.

    A biblioteca `msgspec` é utilizada em vez de `dataclasses` ou `pydantic`
    por ser extremamente rápida e otimizada para serialização e validação
    de dados (similar ao que `protobuf` ou `avro` fariam, mas em Python puro).

    Attributes
    ----------
    id : uuid.UUID
        Identificador único universal (UUID) da instância.  
        Gerado automaticamente com ``uuid4()`` se não informado.  
        Permite rastrear comandos/eventos de forma unívoca em sistemas distribuídos.

    timestamp : datetime.datetime
        Data e hora exata da criação do objeto, sempre em UTC.  
        Essencial para ordenação temporal, auditoria, debugging e mensageria.

    message : str
        Mensagem ou descrição associada ao comando/evento.  
        Útil para logs, depuração, rastreamento ou como metadado adicional.

    connection_id : Optional[uuid.UUID]
        Identificador único da conexão associada ao comando/evento.  
        Pode ser ``None`` caso não haja vínculo direto com uma conexão.  
        Essencial para rastrear interações em sistemas distribuídos e sessões de comunicação.
    """
    id: UUID = field(default_factory=lambda: uuid4())
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    message: str = field(default="")
    connection_id: Optional[UUID] = field(default=None)